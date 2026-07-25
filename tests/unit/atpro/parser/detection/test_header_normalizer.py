"""Tests du normaliseur d'en-tetes."""

from __future__ import annotations

from atpro.parser.detection.header_normalizer import HeaderNormalizer


class TestHeaderNormalizer:
    def test_FEAT_002_2_accents(self) -> None:
        normalizer = HeaderNormalizer()
        assert normalizer.normalize("Numéro Ticket") == "numero_ticket"
        assert normalizer.normalize("  ID de l'appel ") == "id_de_l_appel"

    def test_FEAT_002_2_normalize_many(self) -> None:
        result = HeaderNormalizer().normalize_many(("Nom", "Site Répartition"))
        assert result == ("nom", "site_repartition")
