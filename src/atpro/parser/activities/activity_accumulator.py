"""Accumulateur de metriques pour un agent et un jour.

:spec: FEAT-008.1
:spec: FEAT-009.1
"""

from __future__ import annotations

from datetime import date
from typing import Any

from atpro.domain.value_objects.duration_seconds import DurationSeconds
from atpro.domain.value_objects.percentage import Percentage
from atpro.parser.activities.known_activity_measure import KnownActivityMeasure
from atpro.parser.normalizers.duration_normalizer import DurationNormalizer
from atpro.parser.normalizers.normalization_error import NormalizationError
from atpro.parser.normalizers.percentage_normalizer import PercentageNormalizer
from atpro.parser.results.import_error import ImportError
from atpro.parser.results.import_warning import ImportWarning


class ActivityAccumulator:
    """Consolide les mesures d'une activite journaliere.

    Detecte les doublons identiques (acceptes) et les contradictions
    (``ACTIVITY_MEASURE_CONFLICT``).

    :spec: FEAT-008.1
    :spec: FEAT-009.1
    """

    def __init__(
        self,
        *,
        activity_date: date,
        raw_agent_name: str,
        agent_id: str | None,
        durations: DurationNormalizer | None = None,
        percentages: PercentageNormalizer | None = None,
    ) -> None:
        """Initialise l'accumulateur.

        :param activity_date: Jour d'activite.
        :param raw_agent_name: Nom agent brut.
        :param agent_id: Identifiant stable optionnel.
        :param durations: Parseur de durees.
        :param percentages: Parseur de pourcentages.
        """
        self.activity_date = activity_date
        self.raw_agent_name = raw_agent_name
        self.agent_id = agent_id
        self.row_numbers: list[int] = []
        self._durations = durations or DurationNormalizer()
        self._percentages = percentages or PercentageNormalizer()
        self._raw_by_field: dict[str, str] = {}
        self._counts: dict[str, int] = {}
        self._durations_map: dict[str, DurationSeconds] = {}
        self._percents: dict[str, Percentage | None] = {}
        self.raw_metrics: dict[str, Any] = {}
        self._raw_unknown: dict[str, str] = {}
        self.errors: list[ImportError] = []
        self.warnings: list[ImportWarning] = []

    def note_row(self, row_number: int) -> None:
        """Enregistre une ligne source.

        :param row_number: Numero de ligne CSV.
        """
        if row_number not in self.row_numbers:
            self.row_numbers.append(row_number)

    def add_measure(
        self,
        measure_key: str,
        raw_value: str,
        *,
        row_number: int,
        column: str,
    ) -> None:
        """Ajoute une mesure (connue ou inconnue).

        :param measure_key: Cle normalisee de la mesure / colonne.
        :param raw_value: Valeur brute.
        :param row_number: Ligne CSV.
        :param column: Nom de colonne pour diagnostics.
        :spec: FEAT-009.1
        """
        self.note_row(row_number)
        resolved = KnownActivityMeasure.resolve(measure_key)
        if resolved is None:
            self._add_unknown(
                measure_key, raw_value, row_number=row_number, column=column
            )
            return

        field_name, kind = resolved
        if field_name in self._raw_by_field:
            if self._raw_by_field[field_name] == raw_value:
                return
            self.errors.append(
                ImportError.create(
                    code="ACTIVITY_MEASURE_CONFLICT",
                    message=f"mesure contradictoire: {measure_key}",
                    row_number=row_number,
                    column=column,
                    raw_value=raw_value,
                )
            )
            return

        self._raw_by_field[field_name] = raw_value
        if kind == "count":
            self._parse_count(
                field_name, raw_value, row_number=row_number, column=column
            )
        elif kind == "duration":
            self._parse_duration(
                field_name, raw_value, row_number=row_number, column=column
            )
        else:
            self._parse_percent(
                field_name, raw_value, row_number=row_number, column=column
            )

    def _add_unknown(
        self,
        measure_key: str,
        raw_value: str,
        *,
        row_number: int,
        column: str,
    ) -> None:
        """Conserve une mesure inconnue dans ``raw_metrics``.

        :param measure_key: Cle normalisee.
        :param raw_value: Valeur brute.
        :param row_number: Ligne.
        :param column: Colonne.
        """
        if measure_key in self._raw_unknown:
            if self._raw_unknown[measure_key] == raw_value:
                return
            self.errors.append(
                ImportError.create(
                    code="ACTIVITY_MEASURE_CONFLICT",
                    message=f"mesure contradictoire: {measure_key}",
                    row_number=row_number,
                    column=column,
                    raw_value=raw_value,
                )
            )
            return

        self._raw_unknown[measure_key] = raw_value
        self.raw_metrics[measure_key] = raw_value
        self.warnings.append(
            ImportWarning.create(
                code="ACTIVITY_MEASURE_UNKNOWN",
                message=f"mesure inconnue: {measure_key}",
                row_number=row_number,
                column=column,
                raw_value=measure_key,
            )
        )

    def _parse_count(
        self,
        field_name: str,
        raw_value: str,
        *,
        row_number: int,
        column: str,
    ) -> None:
        """Parse un compteur (vide → 0).

        :param field_name: Champ cible.
        :param raw_value: Valeur brute.
        :param row_number: Ligne.
        :param column: Colonne.
        """
        text = raw_value.strip()
        if text == "":
            self._counts[field_name] = 0
            return
        try:
            self._counts[field_name] = int(text.replace(" ", ""))
        except ValueError:
            self.errors.append(
                ImportError.create(
                    code="ACTIVITY_COUNT_INVALID",
                    message=f"compteur invalide: {raw_value!r}",
                    row_number=row_number,
                    column=column,
                    raw_value=raw_value,
                )
            )

    def _parse_duration(
        self,
        field_name: str,
        raw_value: str,
        *,
        row_number: int,
        column: str,
    ) -> None:
        """Parse une duree (vide → 0 s).

        :param field_name: Champ cible.
        :param raw_value: Valeur brute.
        :param row_number: Ligne.
        :param column: Colonne.
        """
        try:
            parsed = self._durations.parse(raw_value, column=column)
        except NormalizationError as exc:
            self.errors.append(
                ImportError.create(
                    code=exc.code,
                    message=exc.message,
                    row_number=row_number,
                    column=column,
                    raw_value=exc.raw_value,
                )
            )
            return
        self._durations_map[field_name] = parsed or DurationSeconds.from_seconds(0)

    def _parse_percent(
        self,
        field_name: str,
        raw_value: str,
        *,
        row_number: int,
        column: str,
    ) -> None:
        """Parse un pourcentage (vide → ``None``).

        :param field_name: Champ cible.
        :param raw_value: Valeur brute.
        :param row_number: Ligne.
        :param column: Colonne.
        """
        try:
            self._percents[field_name] = self._percentages.parse(
                raw_value, column=column
            )
        except NormalizationError as exc:
            self.errors.append(
                ImportError.create(
                    code=exc.code,
                    message=exc.message,
                    row_number=row_number,
                    column=column,
                    raw_value=exc.raw_value,
                )
            )

    def count_value(self, field_name: str) -> int:
        """Retourne un compteur (defaut 0).

        :param field_name: Champ.
        :returns: Entier.
        """
        return self._counts.get(field_name, 0)

    def duration_value(self, field_name: str) -> DurationSeconds:
        """Retourne une duree (defaut 0 s).

        :param field_name: Champ.
        :returns: Duree.
        """
        return self._durations_map.get(field_name, DurationSeconds.from_seconds(0))

    def percent_value(self, field_name: str) -> Percentage | None:
        """Retourne un pourcentage (defaut ``None``).

        :param field_name: Champ.
        :returns: Pourcentage ou ``None``.
        """
        return self._percents.get(field_name)

    @property
    def has_blocking_errors(self) -> bool:
        """Indique si l'activite ne doit pas etre emise.

        :returns: True si erreurs presentes.
        """
        return bool(self.errors)
