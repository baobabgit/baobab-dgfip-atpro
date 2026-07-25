"""Tests de PercentageNormalizer."""

from __future__ import annotations

import pytest

from atpro.parser.normalizers.normalization_error import NormalizationError
from atpro.parser.normalizers.percentage_normalizer import PercentageNormalizer


class TestPercentageNormalizer:
    def test_FEAT_005_3_percent_with_comma(self) -> None:
        result = PercentageNormalizer().parse("100,00%")
        assert result is not None
        assert result.ratio == pytest.approx(1.0)

    def test_FEAT_005_3_zero_percent(self) -> None:
        result = PercentageNormalizer().parse("0,00%")
        assert result is not None
        assert result.ratio == pytest.approx(0.0)

    def test_FEAT_005_3_without_percent_sign(self) -> None:
        result = PercentageNormalizer().parse("12,5")
        assert result is not None
        assert result.ratio == pytest.approx(0.125)

    def test_FEAT_005_3_empty_returns_none(self) -> None:
        assert PercentageNormalizer().parse(" ") is None

    def test_FEAT_005_3_invalid_percentage(self) -> None:
        with pytest.raises(NormalizationError) as exc_info:
            PercentageNormalizer().parse("n/a")
        assert exc_info.value.code == "PERCENTAGE_INVALID"
