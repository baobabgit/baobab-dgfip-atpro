"""Pourcentage stocke en ratio decimal (0.15 = 15 %).

:spec: FEAT-005.2
"""

from __future__ import annotations

from dataclasses import dataclass

from atpro.domain.exceptions.domain_error import DomainError


@dataclass(frozen=True, slots=True)
class Percentage:
    """Pourcentage represente comme ratio decimal dans ``[0, 1]``.

    Exemple : ``0.155`` represente 15,5 %.

    :param ratio: Ratio decimal.
    :type ratio: float
    :spec: FEAT-005.2
    """

    ratio: float

    def __post_init__(self) -> None:
        """Valide le ratio.

        :raises DomainError: Si le ratio est hors ``[0, 1]``.
        """
        if not 0.0 <= self.ratio <= 1.0:
            raise DomainError(f"ratio de pourcentage hors [0, 1]: {self.ratio}")

    @classmethod
    def from_ratio(cls, value: float) -> Percentage:
        """Cree un pourcentage depuis un ratio.

        :param value: Ratio decimal.
        :returns: Instance valide.
        :raises DomainError: Si hors bornes.
        """
        return cls(ratio=value)

    @classmethod
    def from_percent_string(cls, value: str) -> Percentage:
        """Parse une chaine pourcentage avec virgule ou point.

        ``12,5`` est interprete comme 12,5 % soit un ratio ``0.125``.

        :param value: Chaine numerique.
        :returns: Instance valide.
        :raises DomainError: Si la conversion est impossible.
        """
        text = value.strip().replace("%", "").replace(" ", "")
        if text == "":
            raise DomainError("pourcentage vide")
        normalized = text.replace(",", ".")
        try:
            percent = float(normalized)
        except ValueError as exc:
            raise DomainError(f"pourcentage invalide: {value!r}") from exc
        return cls(ratio=percent / 100.0)
