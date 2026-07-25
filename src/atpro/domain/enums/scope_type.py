"""Enumeration ``ScopeType``.

:spec: FEAT-005.2
"""

from __future__ import annotations

from enum import StrEnum


class ScopeType(StrEnum):
    """Perimetre d'agregation.

    :spec: FEAT-005.2
    """

    SITE = "site"
    AGENT = "agent"
