"""Tests des resultats de parsing."""

from __future__ import annotations

import json

import pytest

from atpro.domain.enums import ImportFileType, ImportSeverity, SchemaVersion
from atpro.domain.exceptions import DomainError
from atpro.domain.value_objects import FileSha256
from atpro.parser.results import (
    FileMetadata,
    ImportError,
    ImportWarning,
    ParseIssue,
    ParsePreview,
    ParseResult,
)


def _metadata() -> FileMetadata:
    return FileMetadata(
        path="appels.csv",
        encoding="utf-8",
        separator=";",
        sha256=FileSha256.from_hex("a" * 64),
        detected_type=ImportFileType.INCOMING_CALLS,
        schema_version=SchemaVersion.V1,
        row_count=2,
        column_names=("ID de l'appel", "Nom de l'agent"),
    )


class TestParseDiagnostics:
    """Issues, warnings et erreurs."""

    def test_FEAT_003_1_issue_with_row(self) -> None:
        issue = ParseIssue(
            code="E001",
            message="duree invalide",
            severity=ImportSeverity.ERROR,
            row_number=3,
            column="duree",
            raw_value="***",
        )
        assert issue.row_number == 3

    def test_FEAT_003_1_issue_without_row(self) -> None:
        issue = ParseIssue(
            code="E002",
            message="fichier vide",
            severity=ImportSeverity.FATAL,
        )
        assert issue.row_number is None

    def test_FEAT_003_1_warning_non_blocking(self) -> None:
        warning = ImportWarning.create(
            code="W001",
            message="colonne inconnue",
            row_number=1,
        )
        assert warning.issue.severity is ImportSeverity.WARNING

    def test_FEAT_003_1_fatal_error(self) -> None:
        error = ImportError.create(
            code="F001",
            message="encodage illisible",
            severity=ImportSeverity.FATAL,
        )
        assert error.issue.severity is ImportSeverity.FATAL

    def test_FEAT_003_1_warning_rejects_error_severity(self) -> None:
        with pytest.raises(DomainError):
            ImportWarning(
                issue=ParseIssue(
                    code="x",
                    message="y",
                    severity=ImportSeverity.ERROR,
                )
            )


class TestParseResult:
    """Resultats et serialisation."""

    def test_FEAT_003_1_result_without_error(self) -> None:
        result = ParseResult.build(
            file_metadata=_metadata(),
            records=({"id": "1"},),
        )
        assert result.summary.error_count == 0
        assert result.summary.record_count == 1

    def test_FEAT_003_1_result_with_warning(self) -> None:
        result = ParseResult.build(
            file_metadata=_metadata(),
            records=({"id": "1"},),
            warnings=(ImportWarning.create(code="W1", message="ok"),),
        )
        assert result.summary.warning_count == 1

    def test_FEAT_003_1_result_with_errors(self) -> None:
        result = ParseResult.build(
            file_metadata=_metadata(),
            errors=(ImportError.create(code="E1", message="ko"),),
        )
        assert result.summary.error_count == 1

    def test_FEAT_003_1_json_stable(self) -> None:
        result = ParseResult.build(file_metadata=_metadata())
        first = result.to_json()
        second = result.to_json()
        assert first == second
        payload = json.loads(first)
        assert payload["detected_type"] == "incoming_calls"
        assert list(payload.keys()) == sorted(payload.keys())

    def test_FEAT_003_1_parse_preview_json(self) -> None:
        preview = ParsePreview(
            file_metadata=_metadata(),
            limit=10,
            records=({"id": "1"},),
            warnings=(),
            errors=(),
        )
        assert "record_count" in json.loads(preview.to_json())
