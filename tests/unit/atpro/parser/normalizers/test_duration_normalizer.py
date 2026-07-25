"""Tests de DurationNormalizer."""

from __future__ import annotations

import pytest

from atpro.parser.normalizers.duration_normalizer import DurationNormalizer
from atpro.parser.normalizers.normalization_error import NormalizationError


class TestDurationNormalizer:
    def test_FEAT_005_3_integer_seconds(self) -> None:
        result = DurationNormalizer().parse("125")
        assert result is not None
        assert result.seconds == 125

    def test_FEAT_005_3_hhmmss(self) -> None:
        result = DurationNormalizer().parse("01:02:03")
        assert result is not None
        assert result.seconds == 3723

    def test_FEAT_005_3_empty_returns_none(self) -> None:
        assert DurationNormalizer().parse("") is None

    def test_FEAT_005_3_negative_duration(self) -> None:
        with pytest.raises(NormalizationError) as exc_info:
            DurationNormalizer().parse("-5")
        assert exc_info.value.code == "DURATION_NEGATIVE"

    def test_FEAT_005_3_invalid_duration(self) -> None:
        with pytest.raises(NormalizationError) as exc_info:
            DurationNormalizer().parse("abc")
        assert exc_info.value.code == "DURATION_INVALID"

    def test_FEAT_005_3_invalid_hhmmss(self) -> None:
        with pytest.raises(NormalizationError) as exc_info:
            DurationNormalizer().parse("99:99:99")
        assert exc_info.value.code == "DURATION_INVALID"
