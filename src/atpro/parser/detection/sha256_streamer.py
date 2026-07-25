"""Calcul d'empreinte SHA-256 en streaming.

:spec: FEAT-002.1
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from atpro.domain.value_objects.file_sha256 import FileSha256

_CHUNK_SIZE = 1024 * 64
_SAMPLE_SIZE = 1024 * 64


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


class Sha256Streamer:
    """Calcule le SHA-256 sans charger tout le fichier en memoire.

    :spec: FEAT-002.1
    """

    def digest(self, path: Path) -> StreamDigestResult:
        """Parcourt le fichier en binaire.

        :param path: Chemin du fichier existant non vide.
        :returns: Empreinte, echantillon et compteur de lignes.
        :raises OSError: Si la lecture echoue.
        """
        hasher = hashlib.sha256()
        sample = bytearray()
        size_bytes = 0
        newline_count = 0
        last_byte: int | None = None

        with path.open("rb") as handle:
            while True:
                chunk = handle.read(_CHUNK_SIZE)
                if not chunk:
                    break
                hasher.update(chunk)
                size_bytes += len(chunk)
                newline_count += chunk.count(b"\n")
                last_byte = chunk[-1]
                if len(sample) < _SAMPLE_SIZE:
                    remaining = _SAMPLE_SIZE - len(sample)
                    sample.extend(chunk[:remaining])

        line_count = newline_count
        if size_bytes > 0 and last_byte not in (None, ord("\n")):
            line_count += 1

        return StreamDigestResult(
            sha256=FileSha256.from_hex(hasher.hexdigest()),
            size_bytes=size_bytes,
            sample=bytes(sample),
            line_count=line_count,
        )
