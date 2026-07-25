"""Tests de CliPresenter."""

from __future__ import annotations

import json

from atpro.domain.enums.import_file_type import ImportFileType
from atpro.domain.enums.schema_version import SchemaVersion
from atpro.domain.value_objects.file_sha256 import FileSha256
from atpro.interfaces.cli.cli_presenter import CliPresenter
from atpro.parser.detection.file_inspection import FileInspection
from atpro.parser.results.file_metadata import FileMetadata
from atpro.parser.results.import_error import ImportError
from atpro.parser.results.import_warning import ImportWarning
from atpro.parser.results.parse_preview import ParsePreview
from atpro.parser.results.parse_result import ParseResult


def _inspection() -> FileInspection:
    return FileInspection(
        path="sample.csv",
        file_name="sample.csv",
        size_bytes=10,
        sha256=FileSha256.from_hex("b" * 64),
        encoding="utf-8",
        encoding_confidence=1.0,
        separator=";",
        separator_confidence=1.0,
        raw_columns=("Numero appelant",),
        normalized_columns=("numero_appelant",),
        lines_read=2,
        detected_type=ImportFileType.INCOMING_CALLS,
        schema_version=SchemaVersion.V1,
        warnings=(ImportWarning.create(code="W1", message="call 0612345678 warn"),),
    )


def _metadata() -> FileMetadata:
    return FileMetadata(
        path="sample.csv",
        encoding="utf-8",
        separator=";",
        sha256=FileSha256.from_hex("b" * 64),
        detected_type=ImportFileType.INCOMING_CALLS,
        schema_version=SchemaVersion.V1,
        row_count=1,
        column_names=("Numero appelant",),
    )


class TestCliPresenter:
    def test_FEAT_002_5_inspection_json(self) -> None:
        text = CliPresenter().format_inspection(_inspection(), as_json=True)
        payload = json.loads(text)
        assert payload["detected_type"] == ImportFileType.INCOMING_CALLS.value

    def test_FEAT_002_5_inspection_human_verbose(self) -> None:
        text = CliPresenter().format_inspection(
            _inspection(), as_json=False, verbose=True
        )
        assert "detected_type:" in text
        assert "warning[W1]" in text
        assert "***" in text  # phone masked

    def test_FEAT_002_5_parse_result_json(self) -> None:
        result = ParseResult.build(file_metadata=_metadata(), records=("r",))
        text = CliPresenter().format_parse_result(result, as_json=True)
        assert json.loads(text)["summary"]["status"] == "success"

    def test_FEAT_002_5_parse_result_verbose(self) -> None:
        result = ParseResult.build(
            file_metadata=_metadata(),
            errors=(ImportError.create(code="E1", message="boom 0611111111"),),
        )
        text = CliPresenter().format_parse_result(result, as_json=False, verbose=True)
        assert "error[E1]" in text
        assert "***" in text

    def test_FEAT_002_5_preview_human(self) -> None:
        preview = ParsePreview(
            file_metadata=_metadata(),
            limit=2,
            records=("rec",),
            warnings=(),
            errors=(),
        )
        text = CliPresenter().format_preview(preview, as_json=False, verbose=True)
        assert "preview_records: 1" in text
        assert "record[1]" in text

    def test_FEAT_002_5_detection_and_technical(self) -> None:
        presenter = CliPresenter()
        assert "FILE_ABSENT" in presenter.format_detection_error(
            "FILE_ABSENT", "missing", as_json=False
        )
        payload = json.loads(
            presenter.format_detection_error("FILE_ABSENT", "missing", as_json=True)
        )
        assert payload["error"]["code"] == "FILE_ABSENT"
        tech = json.loads(presenter.format_technical_error("oops", as_json=True))
        assert tech["error"]["code"] == "TECHNICAL_ERROR"
        assert "TECHNICAL_ERROR" in presenter.format_technical_error(
            "oops", as_json=False
        )

    def test_FEAT_002_5_preview_verbose_issues_and_to_dict(self) -> None:
        class _Record:
            def to_dict(self) -> dict[str, str]:
                return {"id": "A1"}

        class _BadRecord:
            def to_dict(self) -> dict[str, object]:
                return {"bad": object()}

        preview = ParsePreview(
            file_metadata=_metadata(),
            limit=2,
            records=(_Record(), _BadRecord()),
            warnings=(ImportWarning.create(code="W2", message="warn"),),
            errors=(ImportError.create(code="E2", message="err"),),
        )
        text = CliPresenter().format_preview(preview, as_json=False, verbose=True)
        assert '"id": "A1"' in text
        assert "error[E2]" in text
        assert "warning[W2]" in text
        assert "record[2]" in text

    def test_FEAT_002_5_parse_result_verbose_warnings(self) -> None:
        result = ParseResult.build(
            file_metadata=_metadata(),
            records=("r",),
            warnings=(ImportWarning.create(code="W3", message="soft"),),
        )
        text = CliPresenter().format_parse_result(result, as_json=False, verbose=True)
        assert "warning[W3]" in text
