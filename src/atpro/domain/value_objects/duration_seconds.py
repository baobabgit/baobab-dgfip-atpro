"""Duree exprimee en secondes entieres.

:spec: FEAT-005.2
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from atpro.domain.exceptions.domain_error import DomainError

_HHMMSS = re.compile(r"^(\d+):([0-5]?\d):([0-5]?\d)$")


@dataclass(frozen=True, slots=True)
class DurationSeconds:
    """Duree stockee en secondes entieres non negatives.

    :param seconds: Nombre de secondes.
    :type seconds: int
    :spec: FEAT-005.2
    """

    seconds: int

    def __post_init__(self) -> None:
        """Valide la duree.

        :raises DomainError: Si ``seconds`` est negatif.
        """
        if self.seconds < 0:
            raise DomainError(f"duree negative interdite: {self.seconds}")

    @classmethod
    def from_seconds(cls, value: int) -> DurationSeconds:
        """Cree une duree depuis un entier de secondes.

        :param value: Secondes.
        :returns: Instance valide.
        :raises DomainError: Si la valeur est invalide.
        """
        return cls(seconds=value)

    @classmethod
    def from_hhmmss(cls, value: str) -> DurationSeconds:
        """Parse une duree ``HH:MM:SS``.

        :param value: Chaine au format heures:minutes:secondes.
        :returns: Instance valide.
        :raises DomainError: Si le format est invalide.
        """
        text = value.strip()
        match = _HHMMSS.fullmatch(text)
        if match is None:
            raise DomainError(f"duree HH:MM:SS invalide: {value!r}")
        hours = int(match.group(1))
        minutes = int(match.group(2))
        seconds = int(match.group(3))
        total = hours * 3600 + minutes * 60 + seconds
        return cls(seconds=total)
