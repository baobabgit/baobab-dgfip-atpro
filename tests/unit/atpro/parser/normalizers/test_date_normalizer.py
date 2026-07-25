"""Tests de DateNormalizer."""

from __future__ import annotations

from zoneinfo import ZoneInfo

import pytest

from atpro.parser.normalizers.date_normalizer import DateNormalizer
from atpro.parser.normalizers.normalization_error import NormalizationError

_PARIS = ZoneInfo("Europe/Paris")


class TestDateNormalizer:
    def test_FEAT_005_3_dd_mm_yyyy_hhmmss(self) -> None:
        result = DateNormalizer().parse("15/06/2026 14:30:00")
        assert result is not None
        assert result.year == 2026
        assert result.month == 6
        assert result.day == 15
        assert result.hour == 14
        assert result.tzinfo == _PARIS

    def test_FEAT_005_3_dd_mm_yy_hhmmss(self) -> None:
        result = DateNormalizer().parse("15-06-26 09:01:02")
        assert result is not None
        assert result.year == 2026
        assert result.month == 6

    def test_FEAT_005_3_yyyy_mm_dd(self) -> None:
        result = DateNormalizer().parse("2026/06/15")
        assert result is not None
        assert result.day == 15
        assert result.hour == 0

    def test_FEAT_005_3_french_literal(self) -> None:
        result = DateNormalizer().parse("15 juin 2026")
        assert result is not None
        assert result.month == 6
        assert result.day == 15

    def test_FEAT_005_3_empty_returns_none(self) -> None:
        assert DateNormalizer().parse("  ") is None

    def test_FEAT_005_3_invalid_date(self) -> None:
        with pytest.raises(NormalizationError) as exc_info:
            DateNormalizer().parse("not-a-date", column="debut")
        assert exc_info.value.code == "DATE_INVALID"
        assert exc_info.value.column == "debut"
