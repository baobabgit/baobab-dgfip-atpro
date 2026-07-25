"""Tests du detecteur d'encodage."""

from __future__ import annotations

from atpro.parser.detection.encoding_detector import EncodingDetector


class TestEncodingDetector:
    def test_FEAT_002_2_utf8(self) -> None:
        sample = b"Nom de l'agent;Site\n"
        result = EncodingDetector().detect(sample)
        assert result.encoding == "utf-8"
        assert result.confidence == 1.0
        assert result.degraded is False

    def test_FEAT_002_2_utf8_bom(self) -> None:
        sample = b"\xef\xbb\xbf" + b"Nom;Site\n"
        result = EncodingDetector().detect(sample)
        assert result.encoding == "utf-8-sig"

    def test_FEAT_002_2_windows_1252(self) -> None:
        sample = "Num\xe9ro Ticket;Statut\n".encode("cp1252")
        result = EncodingDetector().detect(sample)
        assert result.encoding == "windows-1252"
        assert result.confidence >= 0.8

    def test_FEAT_002_2_degraded_fallback(self) -> None:
        from unittest.mock import patch

        with patch.object(EncodingDetector, "_decodes", return_value=False):
            result = EncodingDetector().detect(b"\x00\x01")
        assert result.degraded is True
        assert result.encoding == "windows-1252"
