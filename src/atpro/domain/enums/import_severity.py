"""Enumeration ``ImportSeverity``.

:spec: FEAT-005.2
"""

from __future__ import annotations

from enum import StrEnum


class ImportSeverity(StrEnum):
    """Severite d'un probleme d'import.

    :spec: FEAT-005.2
    """

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
