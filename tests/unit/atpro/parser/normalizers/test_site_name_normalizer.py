"""Tests de SiteNameNormalizer."""

from __future__ import annotations

from atpro.parser.normalizers.site_name_normalizer import SiteNameNormalizer


class TestSiteNameNormalizer:
    def test_FEAT_010_1_normalizes_site(self) -> None:
        result = SiteNameNormalizer().normalize("  Site  Répartition  ")
        assert result.raw_value == "  Site  Répartition  "
        assert result.normalized_value == "site repartition"
        assert result.first_name_hint is None
        assert result.last_name_hint is None

    def test_FEAT_010_1_empty_site_not_invented(self) -> None:
        result = SiteNameNormalizer().normalize("")
        assert result.normalized_value == ""
        assert result.confidence == 0.0
        assert result.is_ambiguous is True
