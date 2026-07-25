"""Tests de DurationSeconds."""

from __future__ import annotations

import pytest

from atpro.domain.exceptions import DomainError
from atpro.domain.value_objects.duration_seconds import DurationSeconds


class TestDurationSeconds:
    """Conversion et validation des durees."""

    def test_FEAT_005_2_from_seconds(self) -> None:
        assert DurationSeconds.from_seconds(90).seconds == 90

    def test_FEAT_005_2_from_hhmmss(self) -> None:
        assert DurationSeconds.from_hhmmss("01:02:03").seconds == 3723

    def test_FEAT_005_2_reject_negative(self) -> None:
        with pytest.raises(DomainError):
            DurationSeconds.from_seconds(-1)

    def test_FEAT_005_2_reject_invalid_hhmmss(self) -> None:
        with pytest.raises(DomainError):
            DurationSeconds.from_hhmmss("1:99:00")
