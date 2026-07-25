"""Non-regression : erreurs structurees et chemins DomainError.

:spec: FEAT-013.1
"""

from __future__ import annotations

from pathlib import Path

import pytest

from atpro.domain.enums.import_file_type import ImportFileType
from atpro.domain.enums.import_severity import ImportSeverity
from atpro.domain.enums.parse_status import ParseStatus
from atpro.domain.enums.schema_version import SchemaVersion
from atpro.domain.exceptions.domain_error import DomainError
from atpro.domain.value_objects.file_sha256 import FileSha256
from atpro.parser.parse_file_use_case import ParseFileUseCase
from atpro.parser.results.file_metadata import FileMetadata
from atpro.parser.results.import_error import ImportError
from atpro.parser.results.import_warning import ImportWarning
from atpro.parser.results.parse_issue import ParseIssue
from atpro.parser.results.parse_result import ParseResult
from atpro.parser.results.parse_summary import ParseSummary

_FIXTURES_CSV = Path(__file__).resolve().parents[3] / "fixtures" / "csv"
_SHA = FileSha256.from_hex("b" * 64)


def _metadata(**overrides: object) -> FileMetadata:
    values: dict[str, object] = {
        "path": "sample.csv",
        "encoding": "utf-8",
        "separator": ";",
        "sha256": _SHA,
        "detected_type": ImportFileType.TICKETS,
        "schema_version": SchemaVersion.V1,
        "row_count": 1,
        "column_names": ("col",),
    }
    values.update(overrides)
    return FileMetadata(**values)  # type: ignore[arg-type]


class TestNonRegressionErrors:
    """Codes ImportError / ImportWarning et conversion FileDetectionError.

    :spec: FEAT-013.1
    """

    def test_FEAT_013_1_structured_error_codes_from_invalid_fixtures(self) -> None:
        cases = (
            ("incoming_calls_invalid.csv", "CALL_END_BEFORE_START"),
            ("outgoing_calls_invalid.csv", "CALL_END_BEFORE_START"),
            ("tickets_invalid.csv", "TICKET_RESOLVED_BEFORE_CREATED"),
            ("activities_invalid.csv", "ACTIVITY_MEASURE_CONFLICT"),
            ("unknown_format.csv", "FILE_TYPE_UNKNOWN"),
        )
        use_case = ParseFileUseCase()
        for name, expected_code in cases:
            result = use_case.parse(_FIXTURES_CSV / name)
            codes = {error.issue.code for error in result.errors}
            assert (
                expected_code in codes
            ), f"{name}: attendu {expected_code} dans {codes}"

    def test_FEAT_013_1_file_detection_error_via_use_case(self, tmp_path: Path) -> None:
        missing = tmp_path / "missing_nr.csv"
        result = ParseFileUseCase().parse(missing)
        assert result.errors
        assert result.errors[0].issue.code == "FILE_ABSENT"
        assert result.errors[0].issue.severity is ImportSeverity.FATAL
        assert result.summary.status is ParseStatus.FAILED

    def test_FEAT_013_1_empty_file_fatal(self, tmp_path: Path) -> None:
        empty = tmp_path / "empty_nr.csv"
        empty.write_text("", encoding="utf-8")
        result = ParseFileUseCase().parse(empty)
        assert result.errors[0].issue.code == "FILE_EMPTY"
        assert result.errors[0].issue.severity is ImportSeverity.FATAL

    def test_FEAT_013_1_import_error_rejects_warning_severity(self) -> None:
        with pytest.raises(DomainError, match="ImportError"):
            ImportError(
                issue=ParseIssue(
                    code="W",
                    message="warn",
                    severity=ImportSeverity.WARNING,
                )
            )

    def test_FEAT_013_1_import_warning_rejects_fatal_severity(self) -> None:
        with pytest.raises(DomainError, match="ImportWarning"):
            ImportWarning(
                issue=ParseIssue(
                    code="F",
                    message="fatal",
                    severity=ImportSeverity.FATAL,
                )
            )

    def test_FEAT_013_1_import_error_to_dict(self) -> None:
        error = ImportError.create(
            code="E1", message="ko", severity=ImportSeverity.ERROR
        )
        payload = error.to_dict()
        assert payload["issue"]["code"] == "E1"
        assert payload["issue"]["severity"] == ImportSeverity.ERROR.value

    def test_FEAT_013_1_file_metadata_domain_errors(self) -> None:
        with pytest.raises(DomainError, match="path"):
            _metadata(path="   ")
        with pytest.raises(DomainError, match="encoding"):
            _metadata(encoding="")
        with pytest.raises(DomainError, match="separator"):
            _metadata(separator="")
        with pytest.raises(DomainError, match="row_count"):
            _metadata(row_count=-1)

    def test_FEAT_013_1_file_metadata_from_path(self, tmp_path: Path) -> None:
        path = tmp_path / "meta.csv"
        meta = FileMetadata.from_path(
            path,
            encoding="utf-8",
            separator=";",
            sha256=_SHA,
            detected_type=ImportFileType.INCOMING_CALLS,
            schema_version=SchemaVersion.V1,
            row_count=0,
            column_names=("a",),
        )
        assert meta.path == str(path)
        assert meta.row_count == 0

    def test_FEAT_013_1_parse_issue_empty_fields(self) -> None:
        with pytest.raises(DomainError, match="code"):
            ParseIssue(code="  ", message="msg", severity=ImportSeverity.ERROR)
        with pytest.raises(DomainError, match="message"):
            ParseIssue(code="C", message="", severity=ImportSeverity.ERROR)

    def test_FEAT_013_1_parse_summary_negative_counters(self) -> None:
        with pytest.raises(DomainError, match="record_count"):
            ParseSummary(
                status=ParseStatus.SUCCESS,
                record_count=-1,
                warning_count=0,
                error_count=0,
            )

    def test_FEAT_013_1_parse_result_partial_with_errors_and_records(self) -> None:
        result = ParseResult.build(
            file_metadata=_metadata(),
            records=({"id": "1"},),
            errors=(ImportError.create(code="ROW_BAD", message="ligne"),),
        )
        assert result.summary.status is ParseStatus.PARTIAL
        assert result.summary.record_count == 1
        assert result.summary.error_count == 1

    def test_FEAT_013_1_parse_result_partial_warnings_without_records(self) -> None:
        result = ParseResult.build(
            file_metadata=_metadata(),
            records=(),
            warnings=(ImportWarning.create(code="W1", message="info"),),
        )
        assert result.summary.status is ParseStatus.PARTIAL
