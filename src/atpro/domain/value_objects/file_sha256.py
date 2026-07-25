"""Empreinte SHA-256 d'un fichier.

:spec: FEAT-005.2
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from atpro.domain.exceptions.domain_error import DomainError

_SHA256 = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True, slots=True)
class FileSha256:
    """Empreinte SHA-256 hexadecimale en minuscules.

    :param value: Digest hex 64 caracteres.
    :type value: str
    :spec: FEAT-005.2
    """

    value: str

    def __post_init__(self) -> None:
        """Valide le digest.

        :raises DomainError: Si le format est invalide.
        """
        if _SHA256.fullmatch(self.value) is None:
            raise DomainError(f"sha256 invalide: {self.value!r}")

    @classmethod
    def from_hex(cls, value: str) -> FileSha256:
        """Cree une empreinte depuis une chaine hexadecimale.

        :param value: Digest (casse ignoree).
        :returns: Instance normalisee en minuscules.
        :raises DomainError: Si le format est invalide.
        """
        return cls(value=value.strip().lower())
