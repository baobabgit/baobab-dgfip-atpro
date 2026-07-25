"""Tests de Percentage."""

from __future__ import annotations

import pytest

from atpro.domain.exceptions import DomainError
from atpro.domain.value_objects.percentage import Percentage


class TestPercentage:
    """Conversion et validation des pourcentages."""

    def test_FEAT_005_2_percent_with_comma(self) -> None:
        assert Percentage.from_percent_string("12,5").ratio == pytest.approx(0.125)

    def test_FEAT_005_2_from_ratio(self) -> None:
        assert Percentage.from_ratio(0.5).ratio == 0.5

    def test_FEAT_005_2_reject_empty(self) -> None:
        with pytest.raises(DomainError):
            Percentage.from_percent_string("  ")

    def test_FEAT_005_2_reject_out_of_range(self) -> None:
        with pytest.raises(DomainError):
            Percentage.from_ratio(1.5)

    def test_FEAT_005_2_reject_non_numeric(self) -> None:
        with pytest.raises(DomainError):
            Percentage.from_percent_string("abc")
