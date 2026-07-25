"""Mesures d'appel reconnues.

:spec: FEAT-005.4
"""

from __future__ import annotations

from enum import StrEnum


class KnownCallMeasure(StrEnum):
    """Mesures consolidees sur un segment.

    :spec: FEAT-005.4
    """

    TALK = "duree_de_communication"
    HOLD = "duree_de_mise_en_garde"
