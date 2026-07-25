"""Enumeration ``ParseStatus``.

:spec: FEAT-005.2
"""

from __future__ import annotations

from enum import StrEnum


class ParseStatus(StrEnum):
    """Statut global d'un parsing.

    :spec: FEAT-005.2
    """

    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"
    SKIPPED = "skipped"
