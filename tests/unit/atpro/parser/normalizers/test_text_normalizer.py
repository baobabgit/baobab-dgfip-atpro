"""Tests de TextNormalizer."""

from __future__ import annotations

from atpro.parser.normalizers.text_normalizer import TextNormalizer


class TestTextNormalizer:
    def test_FEAT_005_3_collapses_spaces(self) -> None:
        assert TextNormalizer().normalize("  Alice   Dupont  ") == "Alice Dupont"

    def test_FEAT_005_3_accents_for_compare(self) -> None:
        key = TextNormalizer().normalize_for_compare("  Éléonore  ")
        assert key == "eleonore"
