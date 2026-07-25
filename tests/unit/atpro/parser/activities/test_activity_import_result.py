"""Tests de ActivityImportResult."""

from __future__ import annotations

from atpro.parser.activities.activity_import_result import ActivityImportResult


class TestActivityImportResult:
    def test_FEAT_008_1_empty_result(self) -> None:
        result = ActivityImportResult(activities=())
        assert result.activities == ()
        assert result.errors == ()
        assert result.warnings == ()
