"""Tests de ExitCode."""

from __future__ import annotations

from atpro.domain.enums.import_file_type import ImportFileType
from atpro.domain.enums.import_severity import ImportSeverity
from atpro.domain.enums.parse_status import ParseStatus
from atpro.domain.enums.schema_version import SchemaVersion
from atpro.domain.value_objects.file_sha256 import FileSha256
from atpro.interfaces.cli.exit_code import ExitCode
from atpro.parser.results.file_metadata import FileMetadata
from atpro.parser.results.import_error import ImportError
from atpro.parser.results.parse_preview import ParsePreview
from atpro.parser.results.parse_result import ParseResult


def _metadata(
    *,
    detected_type: ImportFileType = ImportFileType.INCOMING_CALLS,
) -> FileMetadata:
    return FileMetadata(
        path="sample.csv",
        encoding="utf-8",
        separator=";",
        sha256=FileSha256.from_hex("a" * 64),
        detected_type=detected_type,
        schema_version=SchemaVersion.V1,
        row_count=1,
        column_names=("col",),
    )


class TestExitCode:
    def test_FEAT_002_5_success(self) -> None:
        result = ParseResult.build(file_metadata=_metadata(), records=("r",))
        assert ExitCode.from_parse_result(result) is ExitCode.SUCCESS
        assert result.summary.status is ParseStatus.SUCCESS

    def test_FEAT_002_5_unknown_format(self) -> None:
        result = ParseResult.build(
            file_metadata=_metadata(detected_type=ImportFileType.UNKNOWN),
            errors=(
                ImportError.create(
                    code="FILE_TYPE_UNKNOWN",
                    message="type inconnu",
                ),
            ),
        )
        assert ExitCode.from_parse_result(result) is ExitCode.UNKNOWN_FORMAT

    def test_FEAT_002_5_fatal_missing(self) -> None:
        result = ParseResult.build(
            file_metadata=_metadata(detected_type=ImportFileType.UNKNOWN),
            errors=(
                ImportError.create(
                    code="FILE_ABSENT",
                    message="absent",
                    severity=ImportSeverity.FATAL,
                ),
            ),
        )
        assert ExitCode.from_parse_result(result) is ExitCode.MISSING_OR_UNREADABLE

    def test_FEAT_002_5_invalid_file(self) -> None:
        result = ParseResult.build(
            file_metadata=_metadata(),
            records=("r",),
            errors=(
                ImportError.create(code="SCHEMA_MISSING_COLUMNS", message="missing"),
            ),
        )
        assert ExitCode.from_parse_result(result) is ExitCode.INVALID_FILE

    def test_FEAT_002_5_from_preview(self) -> None:
        preview = ParsePreview(
            file_metadata=_metadata(detected_type=ImportFileType.UNKNOWN),
            limit=5,
            records=(),
            warnings=(),
            errors=(ImportError.create(code="FILE_TYPE_UNKNOWN", message="unknown"),),
        )
        assert ExitCode.from_parse_preview(preview) is ExitCode.UNKNOWN_FORMAT
