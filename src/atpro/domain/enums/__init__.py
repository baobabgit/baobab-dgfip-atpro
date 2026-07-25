"""Enumerations partagees du domaine.

:spec: FEAT-005.2
"""

from __future__ import annotations

from atpro.domain.enums.call_direction import CallDirection
from atpro.domain.enums.import_file_type import ImportFileType
from atpro.domain.enums.import_severity import ImportSeverity
from atpro.domain.enums.parse_status import ParseStatus
from atpro.domain.enums.period_type import PeriodType
from atpro.domain.enums.schema_version import SchemaVersion
from atpro.domain.enums.scope_type import ScopeType

__all__ = [
    "CallDirection",
    "ImportFileType",
    "ImportSeverity",
    "ParseStatus",
    "PeriodType",
    "SchemaVersion",
    "ScopeType",
]
