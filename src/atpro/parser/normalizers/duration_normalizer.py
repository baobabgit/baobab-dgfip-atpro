"""Parsing des durees CSV.

:spec: FEAT-005.3
"""

from __future__ import annotations

from atpro.domain.exceptions.domain_error import DomainError
from atpro.domain.value_objects.duration_seconds import DurationSeconds
from atpro.parser.normalizers.normalization_error import NormalizationError


class DurationNormalizer:
    """Convertit secondes entieres ou ``HH:MM:SS`` en ``DurationSeconds``.

    :spec: FEAT-005.3
    """

    def parse(self, value: str, *, column: str | None = None) -> DurationSeconds | None:
        """Parse une duree.

        Chaine vide → ``None``.

        :param value: Valeur CSV.
        :param column: Colonne pour le diagnostic.
        :returns: Duree ou ``None``.
        :raises NormalizationError: Si invalide ou negative.
        """
        text = value.strip()
        if text == "":
            return None

        if ":" in text:
            try:
                return DurationSeconds.from_hhmmss(text)
            except DomainError as exc:
                raise NormalizationError(
                    "DURATION_INVALID",
                    str(exc),
                    raw_value=value,
                    column=column,
                ) from exc

        try:
            seconds = int(text.replace(" ", ""))
        except ValueError as exc:
            raise NormalizationError(
                "DURATION_INVALID",
                f"duree invalide: {value!r}",
                raw_value=value,
                column=column,
            ) from exc

        try:
            return DurationSeconds.from_seconds(seconds)
        except DomainError as exc:
            raise NormalizationError(
                "DURATION_NEGATIVE",
                str(exc),
                raw_value=value,
                column=column,
            ) from exc
