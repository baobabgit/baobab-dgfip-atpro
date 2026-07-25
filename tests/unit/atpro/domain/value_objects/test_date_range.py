"""Tests de DateRange."""

from __future__ import annotations

from datetime import date

import pytest

from atpro.domain.exceptions import DomainError
from atpro.domain.value_objects.date_range import DateRange


class TestDateRange:
    """Validation des plages de dates."""

    def test_FEAT_005_2_valid_range(self) -> None:
        rng = DateRange.from_dates(date(2026, 1, 1), date(2026, 1, 31))
        assert rng.start.day == 1
        assert rng.end.day == 31

    def test_FEAT_005_2_invalid_range(self) -> None:
        with pytest.raises(DomainError):
            DateRange.from_dates(date(2026, 2, 1), date(2026, 1, 1))
