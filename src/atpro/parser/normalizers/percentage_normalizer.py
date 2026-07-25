"""Parsing des pourcentages CSV.

:spec: FEAT-005.3
"""

from __future__ import annotations

from atpro.domain.exceptions.domain_error import DomainError
from atpro.domain.value_objects.percentage import Percentage
from atpro.parser.normalizers.normalization_error import NormalizationError


class PercentageNormalizer:
    """Convertit les pourcentages a virgule en ``Percentage``.

    :spec: FEAT-005.3
    """

    def parse(self, value: str, *, column: str | None = None) -> Percentage | None:
        """Parse un pourcentage.

        Chaine vide → ``None``. Accepte ``100,00%`` ou ``12,5`` (sans ``%``).

        :param value: Valeur CSV.
        :param column: Colonne pour le diagnostic.
        :returns: Pourcentage ou ``None``.
        :raises NormalizationError: Si invalide.
        """
        text = value.strip()
        if text == "":
            return None
        try:
            return Percentage.from_percent_string(text)
        except DomainError as exc:
            raise NormalizationError(
                "PERCENTAGE_INVALID",
                str(exc),
                raw_value=value,
                column=column,
            ) from exc
