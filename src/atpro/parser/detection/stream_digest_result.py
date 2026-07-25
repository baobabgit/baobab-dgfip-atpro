"""Resultat du parcours binaire SHA-256.

:spec: FEAT-002.1
"""

from __future__ import annotations

from dataclasses import dataclass

from atpro.domain.value_objects.file_sha256 import FileSha256


@dataclass(frozen=True, slots=True)
class StreamDigestResult:
    """Resultat du passage binaire unique sur le fichier.

    :param sha256: Empreinte hexadecimale.
    :param size_bytes: Taille lue.
    :param sample: Echantillon initial pour detection.
    :param line_count: Nombre de lignes (sauts de ligne comptes).
    :spec: FEAT-002.1
    """

    sha256: FileSha256
    size_bytes: int
    sample: bytes
    line_count: int
