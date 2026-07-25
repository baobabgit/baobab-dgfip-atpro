"""Tests de FileCliService."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

from atpro.domain.enums.import_file_type import ImportFileType
from atpro.domain.enums.schema_version import SchemaVersion
from atpro.domain.value_objects.file_sha256 import FileSha256
from atpro.interfaces.cli.exit_code import ExitCode
from atpro.interfaces.cli.file_cli_service import FileCliService
from atpro.parser.detection.file_detection_error import FileDetectionError
from atpro.parser.detection.file_inspection import FileInspection
from atpro.parser.results.file_metadata import FileMetadata
from atpro.parser.results.import_error import ImportError
from atpro.parser.results.parse_preview import ParsePreview
from atpro.parser.results.parse_result import ParseResult


def _inspection() -> FileInspection:
    return FileInspection(
        path="ok.csv",
        file_name="ok.csv",
        size_bytes=1,
        sha256=FileSha256.from_hex("c" * 64),
        encoding="utf-8",
        encoding_confidence=1.0,
        separator=";",
        separator_confidence=1.0,
        raw_columns=("a",),
        normalized_columns=("a",),
        lines_read=1,
        detected_type=ImportFileType.INCOMING_CALLS,
        schema_version=SchemaVersion.V1,
    )


def _metadata() -> FileMetadata:
    return FileMetadata(
        path="ok.csv",
        encoding="utf-8",
        separator=";",
        sha256=FileSha256.from_hex("c" * 64),
        detected_type=ImportFileType.INCOMING_CALLS,
        schema_version=SchemaVersion.V1,
        row_count=1,
        column_names=("a",),
    )


class TestFileCliService:
    def test_FEAT_002_5_inspect_success(self) -> None:
        use_case = MagicMock()
        use_case.inspect.return_value = _inspection()
        outcome = FileCliService(use_case=use_case).inspect(Path("ok.csv"))
        assert outcome.exit_code is ExitCode.SUCCESS
        assert "incoming_calls" in outcome.text

    def test_FEAT_002_5_inspect_missing(self) -> None:
        use_case = MagicMock()
        use_case.inspect.side_effect = FileDetectionError("FILE_ABSENT", "gone")
        outcome = FileCliService(use_case=use_case).inspect(Path("gone.csv"))
        assert outcome.exit_code is ExitCode.MISSING_OR_UNREADABLE
        assert "FILE_ABSENT" in outcome.text

    def test_FEAT_002_5_inspect_technical(self) -> None:
        use_case = MagicMock()
        use_case.inspect.side_effect = RuntimeError("boom")
        outcome = FileCliService(use_case=use_case).inspect(Path("x.csv"))
        assert outcome.exit_code is ExitCode.TECHNICAL_ERROR

    def test_FEAT_002_5_validate_unknown(self) -> None:
        use_case = MagicMock()
        use_case.validate.return_value = ParseResult.build(
            file_metadata=_metadata(),
            errors=(ImportError.create(code="FILE_TYPE_UNKNOWN", message="unknown"),),
        )
        outcome = FileCliService(use_case=use_case).validate(Path("x.csv"))
        assert outcome.exit_code is ExitCode.UNKNOWN_FORMAT

    def test_FEAT_002_5_preview_success(self) -> None:
        use_case = MagicMock()
        use_case.preview.return_value = ParsePreview(
            file_metadata=_metadata(),
            limit=3,
            records=("a", "b"),
            warnings=(),
            errors=(),
        )
        outcome = FileCliService(use_case=use_case).preview(
            Path("ok.csv"), limit=3, as_json=True
        )
        assert outcome.exit_code is ExitCode.SUCCESS
        assert '"limit": 3' in outcome.text

    def test_FEAT_002_5_validate_technical(self) -> None:
        use_case = MagicMock()
        use_case.validate.side_effect = RuntimeError("fail")
        outcome = FileCliService(use_case=use_case).validate(Path("x.csv"))
        assert outcome.exit_code is ExitCode.TECHNICAL_ERROR

    def test_FEAT_002_5_preview_technical(self) -> None:
        use_case = MagicMock()
        use_case.preview.side_effect = RuntimeError("fail")
        outcome = FileCliService(use_case=use_case).preview(Path("x.csv"))
        assert outcome.exit_code is ExitCode.TECHNICAL_ERROR
