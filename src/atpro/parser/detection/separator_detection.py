"""Resultat de detection de separateur.

:spec: FEAT-002.2
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SeparatorDetection:
    """Separateur CSV detecte sur un echantillon.

    :param separator: Caractere separateur.
    :param confidence: Niveau de confiance dans ``[0.0, 1.0]``.
    :spec: FEAT-002.2
    """

    separator: str
    confidence: float
