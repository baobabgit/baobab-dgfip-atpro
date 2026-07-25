"""Tests de FileSha256."""

from __future__ import annotations

import pytest

from atpro.domain.exceptions import DomainError
from atpro.domain.value_objects.file_sha256 import FileSha256


class TestFileSha256:
    """Validation des empreintes SHA-256."""

    def test_FEAT_005_2_normalize_hex(self) -> None:
        digest = "A" * 64
        assert FileSha256.from_hex(digest).value == "a" * 64

    def test_FEAT_005_2_reject_invalid(self) -> None:
        with pytest.raises(DomainError):
            FileSha256.from_hex("deadbeef")
