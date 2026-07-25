"""Intervalle de dates inclusif.

:spec: FEAT-005.2
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from atpro.domain.exceptions.domain_error import DomainError


@dataclass(frozen=True, slots=True)
class DateRange:
    """Plage de dates avec ``start <= end``.

    :param start: Date de debut.
    :type start: date
    :param end: Date de fin.
    :type end: date
    :spec: FEAT-005.2
    """

    start: date
    end: date

    def __post_init__(self) -> None:
        """Valide l'ordre des bornes.

        :raises DomainError: Si ``start`` est posterieure a ``end``.
        """
        if self.start > self.end:
            raise DomainError(
                f"plage de dates invalide: {self.start.isoformat()} > "
                f"{self.end.isoformat()}"
            )

    @classmethod
    def from_dates(cls, start: date, end: date) -> DateRange:
        """Cree une plage depuis deux dates.

        :param start: Debut.
        :param end: Fin.
        :returns: Instance valide.
        :raises DomainError: Si la plage est invalide.
        """
        return cls(start=start, end=end)
