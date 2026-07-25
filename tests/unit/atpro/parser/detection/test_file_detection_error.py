"""Tests de FileDetectionError."""

from __future__ import annotations

from atpro.parser.detection.file_detection_error import FileDetectionError


class TestFileDetectionError:
    def test_FEAT_002_1_stores_code_and_message(self) -> None:
        error = FileDetectionError("FILE_EMPTY", "fichier vide")
        assert error.code == "FILE_EMPTY"
        assert error.message == "fichier vide"
        assert str(error) == "fichier vide"
