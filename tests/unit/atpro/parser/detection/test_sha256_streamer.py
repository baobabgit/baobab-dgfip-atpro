"""Tests du streamer SHA-256."""

from __future__ import annotations

import hashlib
from pathlib import Path

from atpro.parser.detection.sha256_streamer import Sha256Streamer


class TestSha256Streamer:
    def test_FEAT_002_1_identical_files_same_digest(self, tmp_path: Path) -> None:
        content = b"ID;Nom\n1;Alice\n"
        a = tmp_path / "a.csv"
        b = tmp_path / "b.csv"
        a.write_bytes(content)
        b.write_bytes(content)
        streamer = Sha256Streamer()
        assert streamer.digest(a).sha256 == streamer.digest(b).sha256

    def test_FEAT_002_1_modified_file_changes_digest(self, tmp_path: Path) -> None:
        path = tmp_path / "x.csv"
        path.write_bytes(b"a;b\n1;2\n")
        streamer = Sha256Streamer()
        first = streamer.digest(path).sha256
        path.write_bytes(b"a;b\n1;3\n")
        second = streamer.digest(path).sha256
        assert first != second

    def test_FEAT_002_1_matches_hashlib(self, tmp_path: Path) -> None:
        path = tmp_path / "ref.csv"
        payload = b"colonne;valeur\n" * 1000
        path.write_bytes(payload)
        result = Sha256Streamer().digest(path)
        expected = hashlib.sha256(payload).hexdigest()
        assert result.sha256.value == expected
        assert result.size_bytes == len(payload)
        assert result.line_count == 1000

    def test_FEAT_002_1_counts_last_line_without_newline(self, tmp_path: Path) -> None:
        path = tmp_path / "noln.csv"
        path.write_bytes(b"a;b\n1;2")
        result = Sha256Streamer().digest(path)
        assert result.line_count == 2
