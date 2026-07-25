"""Tests de StreamDigestResult."""

from __future__ import annotations

from atpro.domain.value_objects import FileSha256
from atpro.parser.detection.stream_digest_result import StreamDigestResult


class TestStreamDigestResult:
    def test_FEAT_002_1_stores_fields(self) -> None:
        result = StreamDigestResult(
            sha256=FileSha256.from_hex("c" * 64),
            size_bytes=3,
            sample=b"abc",
            line_count=1,
        )
        assert result.size_bytes == 3
        assert result.sample == b"abc"
