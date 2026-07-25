"""Enumeration ``SchemaVersion``.

:spec: FEAT-005.2
"""

from __future__ import annotations

from enum import StrEnum


class SchemaVersion(StrEnum):
    """Version de schema CSV reconnue.

    :spec: FEAT-005.2
    """

    V1 = "v1"
    UNKNOWN = "unknown"
