"""Construction de ``AgentDailyActivity`` depuis des accumulateurs.

:spec: FEAT-008.1
:spec: FEAT-009.1
"""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from datetime import UTC, date, datetime

from atpro.domain.activities.agent_daily_activity import AgentDailyActivity
from atpro.parser.activities.activity_accumulator import ActivityAccumulator
from atpro.parser.activities.activity_import_result import ActivityImportResult
from atpro.parser.activities.known_activity_measure import KnownActivityMeasure
from atpro.parser.detection.header_normalizer import HeaderNormalizer
from atpro.parser.normalizers.agent_name_normalizer import AgentNameNormalizer
from atpro.parser.normalizers.date_normalizer import DateNormalizer
from atpro.parser.normalizers.duration_normalizer import DurationNormalizer
from atpro.parser.normalizers.normalization_error import NormalizationError
from atpro.parser.normalizers.percentage_normalizer import PercentageNormalizer
from atpro.parser.results.import_error import ImportError
from atpro.parser.results.import_warning import ImportWarning


class ActivityBuilder:
    """Construit des ``AgentDailyActivity`` a partir de cellules CSV.

    :spec: FEAT-008.1
    :spec: FEAT-009.1
    """

    def __init__(
        self,
        *,
        dates: DateNormalizer | None = None,
        durations: DurationNormalizer | None = None,
        percentages: PercentageNormalizer | None = None,
        agents: AgentNameNormalizer | None = None,
        headers: HeaderNormalizer | None = None,
    ) -> None:
        """Injecte les collaborateurs.

        :param dates: Normaliseur de dates.
        :param durations: Normaliseur de durees.
        :param percentages: Normaliseur de pourcentages.
        :param agents: Normaliseur d'agents.
        :param headers: Normaliseur d'en-tetes / mesures.
        """
        self._dates = dates or DateNormalizer()
        self._durations = durations or DurationNormalizer()
        self._percentages = percentages or PercentageNormalizer()
        self._agents = agents or AgentNameNormalizer()
        self._headers = headers or HeaderNormalizer()

    def create_accumulator(
        self,
        *,
        periode_raw: str | None,
        agent_raw: str | None,
        row_number: int,
    ) -> tuple[ActivityAccumulator | None, list[ImportError], list[ImportWarning]]:
        """Cree un accumulateur pour une paire date/agent.

        :param periode_raw: Periode brute.
        :param agent_raw: Nom agent brut.
        :param row_number: Ligne CSV.
        :returns: Accumulateur optionnel et diagnostics.
        """
        errors: list[ImportError] = []
        warnings: list[ImportWarning] = []

        if periode_raw is None or not periode_raw.strip():
            errors.append(
                ImportError.create(
                    code="ACTIVITY_DATE_REQUIRED",
                    message="periode absente",
                    row_number=row_number,
                    column="periode",
                )
            )
            return None, errors, warnings

        try:
            parsed = self._dates.parse(periode_raw, column="periode")
        except NormalizationError as exc:
            errors.append(
                ImportError.create(
                    code=exc.code,
                    message=exc.message,
                    row_number=row_number,
                    column="periode",
                    raw_value=exc.raw_value,
                )
            )
            return None, errors, warnings

        if parsed is None:
            errors.append(
                ImportError.create(
                    code="ACTIVITY_DATE_REQUIRED",
                    message="periode absente",
                    row_number=row_number,
                    column="periode",
                )
            )
            return None, errors, warnings

        activity_date: date = parsed.date()

        if agent_raw is None or not agent_raw.strip():
            errors.append(
                ImportError.create(
                    code="ACTIVITY_AGENT_REQUIRED",
                    message="agent absent",
                    row_number=row_number,
                    column="agent_groupe_agent",
                )
            )
            return None, errors, warnings

        identity = self._agents.normalize(agent_raw)
        if identity.normalized_value == "":
            errors.append(
                ImportError.create(
                    code="ACTIVITY_AGENT_REQUIRED",
                    message="agent vide",
                    row_number=row_number,
                    column="agent_groupe_agent",
                )
            )
            return None, errors, warnings

        if identity.is_ambiguous:
            warnings.append(
                ImportWarning.create(
                    code="ACTIVITY_AGENT_AMBIGUOUS",
                    message="rapprochement agent ambigu",
                    row_number=row_number,
                    column="agent_groupe_agent",
                    raw_value=agent_raw,
                )
            )

        agent_id = f"agent:{identity.normalized_value}"
        accumulator = ActivityAccumulator(
            activity_date=activity_date,
            raw_agent_name=agent_raw.strip(),
            agent_id=agent_id,
            durations=self._durations,
            percentages=self._percentages,
        )
        accumulator.note_row(row_number)
        return accumulator, errors, warnings

    def apply_wide_row(
        self,
        accumulator: ActivityAccumulator,
        cells: dict[str, str],
        *,
        row_number: int,
        already_normalized_keys: bool = False,
    ) -> None:
        """Injecte toutes les colonnes d'une ligne format large.

        :param accumulator: Accumulateur cible.
        :param cells: Cellules.
        :param row_number: Ligne.
        :param already_normalized_keys: Cles deja normalisees.
        :spec: FEAT-008.1
        """
        normalized = self._normalize_cells(cells, already_normalized_keys)
        for key, value in normalized.items():
            if KnownActivityMeasure.is_meta_column(key) or key == "":
                continue
            accumulator.add_measure(
                key,
                value,
                row_number=row_number,
                column=key,
            )

    def apply_long_measure(
        self,
        accumulator: ActivityAccumulator,
        *,
        measure_name: str | None,
        measure_value: str | None,
        row_number: int,
    ) -> None:
        """Injecte une mesure format long.

        :param accumulator: Accumulateur cible.
        :param measure_name: Libelle mesure brut.
        :param measure_value: Valeur brute.
        :param row_number: Ligne.
        :spec: FEAT-009.1
        """
        if measure_name is None or not measure_name.strip():
            accumulator.warnings.append(
                ImportWarning.create(
                    code="ACTIVITY_MEASURE_MISSING",
                    message="nom de mesure absent",
                    row_number=row_number,
                    column="noms_de_mesures",
                )
            )
            return
        key = self._headers.normalize(measure_name)
        accumulator.add_measure(
            key,
            measure_value or "",
            row_number=row_number,
            column="valeurs_de_mesures",
        )

    def build(
        self,
        accumulators: Sequence[ActivityAccumulator],
        *,
        now: datetime | None = None,
    ) -> ActivityImportResult:
        """Produit les activites et agrege les diagnostics.

        :param accumulators: Accumulateurs remplis.
        :param now: Horodatage (tests).
        :returns: Resultat d'import.
        :spec: FEAT-008.1
        :spec: FEAT-009.1
        """
        created_at = now or datetime.now(tz=UTC)
        activities: list[AgentDailyActivity] = []
        errors: list[ImportError] = []
        warnings: list[ImportWarning] = []

        for acc in accumulators:
            errors.extend(acc.errors)
            warnings.extend(acc.warnings)
            if acc.has_blocking_errors:
                continue
            activities.append(self._to_activity(acc, created_at))

        return ActivityImportResult(
            activities=tuple(activities),
            errors=tuple(errors),
            warnings=tuple(warnings),
        )

    def _to_activity(
        self, acc: ActivityAccumulator, created_at: datetime
    ) -> AgentDailyActivity:
        """Convertit un accumulateur en modele domaine.

        :param acc: Accumulateur.
        :param created_at: Horodatage.
        :returns: Activite.
        """
        fingerprint = self._stable_id(
            "line",
            acc.activity_date.isoformat(),
            acc.raw_agent_name,
            ",".join(str(n) for n in acc.row_numbers),
        )
        activity_id = self._stable_id(
            "activity",
            acc.activity_date.isoformat(),
            acc.agent_id or acc.raw_agent_name,
        )
        raw_metrics = dict(acc.raw_metrics) if acc.raw_metrics else None
        return AgentDailyActivity(
            id=activity_id,
            agent_id=acc.agent_id,
            raw_agent_name=acc.raw_agent_name,
            site_id=None,
            activity_date=acc.activity_date,
            received_calls=acc.count_value("received_calls"),
            answered_calls=acc.count_value("answered_calls"),
            outgoing_calls=acc.count_value("outgoing_calls"),
            transferred_in_calls=acc.count_value("transferred_in_calls"),
            handled_calls_total=acc.count_value("handled_calls_total"),
            transferred_calls=acc.count_value("transferred_calls"),
            hold_count=acc.count_value("hold_count"),
            consultation_count=acc.count_value("consultation_count"),
            login_time_seconds=acc.duration_value("login_time_seconds"),
            ready_time_seconds=acc.duration_value("ready_time_seconds"),
            not_ready_time_seconds=acc.duration_value("not_ready_time_seconds"),
            phone_time_seconds=acc.duration_value("phone_time_seconds"),
            incoming_talk_time_seconds=acc.duration_value("incoming_talk_time_seconds"),
            outgoing_talk_time_seconds=acc.duration_value("outgoing_talk_time_seconds"),
            after_call_work_seconds=acc.duration_value("after_call_work_seconds"),
            rona_time_seconds=acc.duration_value("rona_time_seconds"),
            hold_duration_seconds=acc.duration_value("hold_duration_seconds"),
            answer_rate=acc.percent_value("answer_rate"),
            hold_rate=acc.percent_value("hold_rate"),
            raw_metrics=raw_metrics,
            source_import_batch_id=None,
            line_fingerprint=fingerprint,
            created_at=created_at,
        )

    def _normalize_cells(
        self, cells: dict[str, str], already_normalized_keys: bool
    ) -> dict[str, str]:
        """Normalise les cles de cellules.

        :param cells: Cellules.
        :param already_normalized_keys: Si True, ne renormalise pas.
        :returns: Dictionnaire normalise.
        """
        if already_normalized_keys:
            return cells
        return {self._headers.normalize(key): value for key, value in cells.items()}

    def normalize_header(self, header: str) -> str:
        """Expose la normalisation d'en-tete.

        :param header: Libelle brut.
        :returns: Cle normalisee.
        """
        return self._headers.normalize(header)

    def cell(
        self, cells: dict[str, str], key: str, *, already_normalized_keys: bool = False
    ) -> str | None:
        """Lit une cellule optionnelle.

        :param cells: Cellules.
        :param key: Cle normalisee attendue.
        :param already_normalized_keys: Cles deja normalisees.
        :returns: Valeur strippee ou ``None``.
        """
        text = self.raw_cell(
            cells, key, already_normalized_keys=already_normalized_keys
        )
        if text is None:
            return None
        stripped = text.strip()
        return stripped if stripped else None

    def raw_cell(
        self, cells: dict[str, str], key: str, *, already_normalized_keys: bool = False
    ) -> str | None:
        """Lit une cellule en conservant la chaine vide.

        :param cells: Cellules.
        :param key: Cle normalisee attendue.
        :param already_normalized_keys: Cles deja normalisees.
        :returns: Valeur brute ou ``None`` si cle absente.
        """
        normalized = self._normalize_cells(cells, already_normalized_keys)
        if key not in normalized:
            return None
        return normalized[key]

    def group_key(self, *, periode_raw: str, agent_raw: str) -> tuple[date, str] | None:
        """Calcule la cle de regroupement date/agent (format long).

        :param periode_raw: Periode.
        :param agent_raw: Agent.
        :returns: Cle ou ``None`` si invalide.
        """
        try:
            parsed = self._dates.parse(periode_raw, column="periode")
        except NormalizationError:
            return None
        if parsed is None:
            return None
        identity = self._agents.normalize(agent_raw)
        if identity.normalized_value == "":
            return None
        return parsed.date(), identity.normalized_value

    @staticmethod
    def _stable_id(prefix: str, *parts: str) -> str:
        """Identifiant deterministe.

        :param prefix: Prefixe.
        :param parts: Parties.
        :returns: Identifiant.
        """
        digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:16]
        return f"{prefix}-{digest}"
