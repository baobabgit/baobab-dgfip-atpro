"""Tests de FileInspection."""

from __future__ import annotations

import pytest

from atpro.domain.exceptions import DomainError
from atpro.domain.value_objects import FileSha256
from atpro.parser.detection.file_inspection import FileInspection


def _inspection(**overrides: object) -> FileInspection:
    payload: dict[str, object] = {
        "path": "/tmp/a.csv",
        "file_name": "a.csv",
        "size_bytes": 10,
        "sha256": FileSha256.from_hex("b" * 64),
        "encoding": "utf-8",
        "encoding_confidence": 1.0,
        "separator": ";",
        "separator_confidence": 0.9,
        "raw_columns": ("Nom",),
        "normalized_columns": ("nom",),
        "lines_read": 2,
    }
    payload.update(overrides)
    return FileInspection(**payload)  # type: ignore[arg-type]


class TestFileInspection:
    def test_FEAT_002_1_to_dict_serializes(self) -> None:
        data = _inspection().to_dict()
        assert data["sha256"] == "b" * 64
        assert data["detected_type"] == "unknown"
        assert data["raw_columns"] == ["Nom"]

    def test_FEAT_002_1_rejects_desynced_columns(self) -> None:
        with pytest.raises(DomainError):
            _inspection(normalized_columns=("a", "b"))

    def test_FEAT_002_1_rejects_invalid_bounds(self) -> None:
        with pytest.raises(DomainError):
            _inspection(path=" ")
        with pytest.raises(DomainError):
            _inspection(size_bytes=-1)
        with pytest.raises(DomainError):
            _inspection(encoding_confidence=1.5)
        with pytest.raises(DomainError):
            _inspection(separator_confidence=-0.1)
        with pytest.raises(DomainError):
            _inspection(lines_read=-2)
