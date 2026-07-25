"""Tests de NormalizationError."""

from __future__ import annotations

from atpro.parser.normalizers.normalization_error import NormalizationError


class TestNormalizationError:
    def test_FEAT_005_3_stores_fields(self) -> None:
        error = NormalizationError(
            "DATE_INVALID",
            "date invalide",
            raw_value="xx",
            column="debut",
        )
        assert error.code == "DATE_INVALID"
        assert error.column == "debut"
        assert str(error) == "date invalide"
