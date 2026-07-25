"""Consolidation des lignes d'appel en Call / CallSegment.

:spec: FEAT-005.4
"""

from __future__ import annotations

import hashlib
from collections import defaultdict
from collections.abc import Sequence
from datetime import UTC, datetime

from atpro.domain.calls.call import Call
from atpro.domain.calls.call_segment import CallSegment
from atpro.domain.enums.call_direction import CallDirection
from atpro.domain.enums.import_severity import ImportSeverity
from atpro.domain.value_objects.duration_seconds import DurationSeconds
from atpro.parser.calls.call_consolidation_result import CallConsolidationResult
from atpro.parser.calls.known_call_measure import KnownCallMeasure
from atpro.parser.calls.phone_hasher import PhoneHasher
from atpro.parser.calls.raw_call_row import RawCallRow
from atpro.parser.detection.header_normalizer import HeaderNormalizer
from atpro.parser.normalizers.date_normalizer import DateNormalizer
from atpro.parser.normalizers.duration_normalizer import DurationNormalizer
from atpro.parser.normalizers.normalization_error import NormalizationError
from atpro.parser.results.import_error import ImportError
from atpro.parser.results.import_warning import ImportWarning


class CallConsolidator:
    """Groupe les lignes et consolide les mesures par segment.

    :spec: FEAT-005.4
    """

    def __init__(
        self,
        *,
        date_normalizer: DateNormalizer | None = None,
        duration_normalizer: DurationNormalizer | None = None,
        header_normalizer: HeaderNormalizer | None = None,
        phone_hasher: PhoneHasher | None = None,
    ) -> None:
        """Injecte les collaborateurs.

        :param date_normalizer: Parseur de dates.
        :param duration_normalizer: Parseur de durees.
        :param header_normalizer: Normaliseur de libelles de mesures.
        :param phone_hasher: Hacheur de numeros.
        """
        self._dates = date_normalizer or DateNormalizer()
        self._durations = duration_normalizer or DurationNormalizer()
        self._headers = header_normalizer or HeaderNormalizer()
        self._phones = phone_hasher or PhoneHasher()

    def consolidate(
        self,
        rows: Sequence[RawCallRow],
        *,
        direction: CallDirection,
        source_system: str = "csv",
        now: datetime | None = None,
    ) -> CallConsolidationResult:
        """Consolide un lot de lignes brutes.

        :param rows: Lignes mappees.
        :param direction: Sens de l'appel.
        :param source_system: Systeme source.
        :param now: Horodatage de creation (tests).
        :returns: Appels, segments et diagnostics.
        :spec: FEAT-005.4
        """
        created_at = now or datetime.now(tz=UTC)
        errors: list[ImportError] = []
        warnings: list[ImportWarning] = []
        grouped: dict[tuple[str, str, str, str], list[RawCallRow]] = defaultdict(list)
        call_meta: dict[str, RawCallRow] = {}

        for row in rows:
            if not row.external_call_id:
                errors.append(
                    ImportError.create(
                        code="CALL_ID_MISSING",
                        message="identifiant appel absent",
                        row_number=row.row_number,
                        column="id_de_l_appel",
                    )
                )
                continue

            call_id = row.external_call_id
            if call_id not in call_meta:
                call_meta[call_id] = row

            agent_key = (row.agent_name or "").strip()
            if not agent_key:
                warnings.append(
                    ImportWarning.create(
                        code="CALL_AGENT_EMPTY",
                        message="agent vide sur la ligne d'appel",
                        row_number=row.row_number,
                        column="nom_de_l_agent",
                        severity=ImportSeverity.WARNING,
                    )
                )

            segment_key = (
                call_id,
                agent_key,
                row.started_at_raw or "",
                row.ended_at_raw or "",
            )
            grouped[segment_key].append(row)

        calls: list[Call] = []
        segments: list[CallSegment] = []
        call_ids_built: set[str] = set()
        segment_index_by_call: dict[str, int] = defaultdict(int)

        for segment_key, segment_rows in grouped.items():
            external_id, agent_key, start_raw, end_raw = segment_key
            sample = segment_rows[0]
            internal_call_id = self._stable_id("call", external_id, direction.value)

            started_at, ended_at, date_errors = self._parse_window(
                sample, start_raw, end_raw
            )
            errors.extend(date_errors)
            if started_at is None:
                continue

            talk, hold, measure_errors, measure_warnings = self._consolidate_measures(
                segment_rows
            )
            errors.extend(measure_errors)
            warnings.extend(measure_warnings)
            if measure_errors:
                continue

            if external_id not in call_ids_built:
                meta = call_meta[external_id]
                calls.append(
                    Call(
                        id=internal_call_id,
                        source_system=source_system,
                        external_call_id=external_id,
                        direction=direction,
                        started_at=started_at,
                        ended_at=ended_at,
                        caller_hash=self._phones.hash(meta.caller),
                        callee_hash=self._phones.hash(meta.callee),
                        flow=meta.flow,
                        service=meta.service,
                        global_result=None,
                        source_import_batch_id=None,
                        created_at=created_at,
                        updated_at=created_at,
                        line_fingerprint=None,
                    )
                )
                call_ids_built.add(external_id)

            index = segment_index_by_call[external_id]
            segment_index_by_call[external_id] = index + 1
            segment_id = self._stable_id(
                "seg",
                external_id,
                agent_key,
                start_raw,
                end_raw,
                str(index),
            )
            segments.append(
                CallSegment(
                    id=segment_id,
                    call_id=internal_call_id,
                    segment_index=index,
                    agent_id=None,
                    raw_agent_name=agent_key,
                    site_id=None,
                    started_at=started_at,
                    ended_at=ended_at,
                    talk_duration_seconds=talk,
                    hold_duration_seconds=hold,
                    qualification_category=sample.qualification_category,
                    qualification_reason=sample.qualification_reason,
                    hangup_origin=sample.hangup_origin,
                    source_row_numbers=tuple(r.row_number for r in segment_rows),
                    line_fingerprint=None,
                    created_at=created_at,
                )
            )

        for call in calls:
            related = [s for s in segments if s.call_id == call.id]
            if len(related) > 1:
                warnings.append(
                    ImportWarning.create(
                        code="CALL_MULTI_SEGMENT",
                        message=(
                            f"appel multi-segments detecte: " f"{call.external_call_id}"
                        ),
                    )
                )

        return CallConsolidationResult(
            calls=tuple(calls),
            segments=tuple(segments),
            errors=tuple(errors),
            warnings=tuple(warnings),
        )

    def _parse_window(
        self,
        sample: RawCallRow,
        start_raw: str,
        end_raw: str,
    ) -> tuple[datetime | None, datetime | None, list[ImportError]]:
        """Parse debut/fin et valide l'ordre.

        :returns: Debut, fin, erreurs.
        """
        errors: list[ImportError] = []
        try:
            started_at = self._dates.parse(start_raw, column="debut_d_appel")
        except NormalizationError as exc:
            errors.append(
                ImportError.create(
                    code=exc.code,
                    message=exc.message,
                    row_number=sample.row_number,
                    column="debut_d_appel",
                    raw_value=exc.raw_value,
                )
            )
            started_at = None

        ended_at: datetime | None = None
        if end_raw:
            try:
                ended_at = self._dates.parse(end_raw, column="fin_d_appel")
            except NormalizationError as exc:
                errors.append(
                    ImportError.create(
                        code=exc.code,
                        message=exc.message,
                        row_number=sample.row_number,
                        column="fin_d_appel",
                        raw_value=exc.raw_value,
                    )
                )

        if started_at is None and not errors:
            errors.append(
                ImportError.create(
                    code="CALL_START_MISSING",
                    message="debut d'appel absent ou invalide",
                    row_number=sample.row_number,
                    column="debut_d_appel",
                )
            )

        if started_at is not None and ended_at is not None and ended_at < started_at:
            errors.append(
                ImportError.create(
                    code="CALL_END_BEFORE_START",
                    message="fin avant debut",
                    row_number=sample.row_number,
                )
            )
            return None, None, errors

        return started_at, ended_at, errors

    def _consolidate_measures(self, rows: Sequence[RawCallRow]) -> tuple[
        DurationSeconds,
        DurationSeconds,
        list[ImportError],
        list[ImportWarning],
    ]:
        """Fusionne les mesures d'un segment.

        :returns: Talk, hold, erreurs, warnings.
        """
        errors: list[ImportError] = []
        warnings: list[ImportWarning] = []
        talk: DurationSeconds | None = None
        hold: DurationSeconds | None = None
        seen: dict[str, str] = {}

        for row in rows:
            if not row.measure_name:
                continue
            measure_key = self._headers.normalize(row.measure_name)
            raw_value = row.measure_value or ""

            if measure_key in seen and seen[measure_key] != raw_value:
                errors.append(
                    ImportError.create(
                        code="CALL_MEASURE_CONFLICT",
                        message=(f"mesure contradictoire: {row.measure_name}"),
                        row_number=row.row_number,
                        column="valeurs_de_mesures",
                        raw_value=raw_value,
                    )
                )
                continue
            seen[measure_key] = raw_value

            if measure_key == KnownCallMeasure.TALK:
                try:
                    parsed = self._durations.parse(
                        raw_value, column="valeurs_de_mesures"
                    )
                except NormalizationError as exc:
                    errors.append(
                        ImportError.create(
                            code=exc.code,
                            message=exc.message,
                            row_number=row.row_number,
                            column="valeurs_de_mesures",
                            raw_value=exc.raw_value,
                        )
                    )
                    continue
                talk = parsed or DurationSeconds.from_seconds(0)
            elif measure_key == KnownCallMeasure.HOLD:
                try:
                    parsed = self._durations.parse(
                        raw_value, column="valeurs_de_mesures"
                    )
                except NormalizationError as exc:
                    errors.append(
                        ImportError.create(
                            code=exc.code,
                            message=exc.message,
                            row_number=row.row_number,
                            column="valeurs_de_mesures",
                            raw_value=exc.raw_value,
                        )
                    )
                    continue
                hold = parsed or DurationSeconds.from_seconds(0)
            else:
                warnings.append(
                    ImportWarning.create(
                        code="CALL_MEASURE_UNKNOWN",
                        message=f"mesure inconnue: {row.measure_name}",
                        row_number=row.row_number,
                        column="noms_de_mesures",
                        raw_value=row.measure_name,
                    )
                )

        return (
            talk or DurationSeconds.from_seconds(0),
            hold or DurationSeconds.from_seconds(0),
            errors,
            warnings,
        )

    @staticmethod
    def _stable_id(prefix: str, *parts: str) -> str:
        """Construit un identifiant deterministe.

        :param prefix: Prefixe.
        :param parts: Parties de cle.
        :returns: Identifiant.
        """
        digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:16]
        return f"{prefix}-{digest}"
