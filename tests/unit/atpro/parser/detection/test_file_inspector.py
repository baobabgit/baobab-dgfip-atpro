"""Tests du service FileInspector."""

from __future__ import annotations

from pathlib import Path

import pytest

from atpro.parser.detection.encoding_detection import EncodingDetection
from atpro.parser.detection.encoding_detector import EncodingDetector
from atpro.parser.detection.file_detection_error import FileDetectionError
from atpro.parser.detection.file_inspector import FileInspector


class TestFileInspector:
    def test_FEAT_002_1_utf8_file(self, tmp_path: Path) -> None:
        path = tmp_path / "appels.csv"
        path.write_text(
            "ID de l'appel;Nom de l'agent\n1;Alice\n",
            encoding="utf-8",
        )
        inspection = FileInspector().inspect(path)
        assert inspection.encoding == "utf-8"
        assert inspection.separator == ";"
        assert inspection.raw_columns[0] == "ID de l'appel"
        assert inspection.normalized_columns[0] == "id_de_l_appel"
        assert inspection.size_bytes > 0
        assert len(inspection.sha256.value) == 64

    def test_FEAT_002_2_windows_1252_file(self, tmp_path: Path) -> None:
        path = tmp_path / "tickets.csv"
        content = "Numéro Ticket;Statut Ticket\nT-1;Ouvert\n"
        path.write_bytes(content.encode("cp1252"))
        inspection = FileInspector().inspect(path)
        assert inspection.encoding == "windows-1252"
        assert "Numero Ticket" in inspection.raw_columns[0] or "Numéro" in (
            inspection.raw_columns[0]
        )
        assert inspection.normalized_columns[0] == "numero_ticket"

    def test_FEAT_002_2_semicolon_separator(self, tmp_path: Path) -> None:
        path = tmp_path / "data.csv"
        path.write_text("a;b;c\n1;2;3\n", encoding="utf-8")
        inspection = FileInspector().inspect(path)
        assert inspection.separator == ";"

    def test_FEAT_002_1_empty_file(self, tmp_path: Path) -> None:
        path = tmp_path / "empty.csv"
        path.write_bytes(b"")
        with pytest.raises(FileDetectionError) as exc_info:
            FileInspector().inspect(path)
        assert exc_info.value.code == "FILE_EMPTY"

    def test_FEAT_002_1_absent_file(self, tmp_path: Path) -> None:
        path = tmp_path / "missing.csv"
        with pytest.raises(FileDetectionError) as exc_info:
            FileInspector().inspect(path)
        assert exc_info.value.code == "FILE_ABSENT"

    def test_FEAT_002_2_malencoded_headers_still_readable(self, tmp_path: Path) -> None:
        path = tmp_path / "broken.csv"
        # Octets cp1252 lus ensuite via detection.
        path.write_bytes("Répartition;Agent\nA;B\n".encode("cp1252"))
        inspection = FileInspector().inspect(path)
        assert inspection.normalized_columns[0] == "repartition"
        assert inspection.lines_read >= 2

    def test_FEAT_002_2_degraded_encoding_warning(self, tmp_path: Path) -> None:
        path = tmp_path / "plain.csv"
        path.write_text("a;b\n1;2\n", encoding="utf-8")

        class _Degraded(EncodingDetector):
            def detect(self, sample: bytes) -> EncodingDetection:
                assert sample
                return EncodingDetection(
                    encoding="windows-1252",
                    confidence=0.35,
                    degraded=True,
                )

        inspection = FileInspector(encoding_detector=_Degraded()).inspect(path)
        assert any(w.issue.code == "ENC_DEGRADED" for w in inspection.warnings)

    def test_FEAT_002_2_missing_header_warning(self, tmp_path: Path) -> None:
        path = tmp_path / "blanks.csv"
        path.write_bytes(b"\n\n\n")
        inspection = FileInspector().inspect(path)
        assert any(w.issue.code == "HEADER_MISSING" for w in inspection.warnings)
