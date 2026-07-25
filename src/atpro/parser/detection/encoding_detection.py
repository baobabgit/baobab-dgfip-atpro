"""Resultat de detection d'encodage.

:spec: FEAT-002.2
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EncodingDetection:
    """Encodage detecte sur un echantillon.

    :param encoding: Nom codec Python (ex. ``utf-8``, ``windows-1252``).
    :param confidence: Niveau de confiance dans ``[0.0, 1.0]``.
    :param degraded: True si fallback peu fiable.
    :spec: FEAT-002.2
    """

    encoding: str
    confidence: float
    degraded: bool = False
