"""Enumeration ``PeriodType``.

:spec: FEAT-005.2
"""

from __future__ import annotations

from enum import StrEnum


class PeriodType(StrEnum):
    """Granularite temporelle d'une periode.

    :spec: FEAT-005.2
    """

    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"
    CUSTOM = "custom"
