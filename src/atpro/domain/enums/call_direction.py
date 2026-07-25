"""Enumeration ``CallDirection``.

:spec: FEAT-005.2
"""

from __future__ import annotations

from enum import StrEnum


class CallDirection(StrEnum):
    """Sens d'un appel telephonique.

    :spec: FEAT-005.2
    """

    INCOMING = "incoming"
    OUTGOING = "outgoing"
