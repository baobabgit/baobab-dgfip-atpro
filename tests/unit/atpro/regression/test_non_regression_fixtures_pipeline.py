"""Non-regression : pipeline ParseFileUseCase sur fixtures CSV.

:spec: FEAT-013.1
"""

from __future__ import annotations

from pathlib import Path

import pytest

from atpro.domain.enums.import_file_type import ImportFileType
from atpro.domain.enums.import_severity import ImportSeverity
from atpro.parser.parse_file_use_case import ParseFileUseCase

_FIXTURES_CSV = Path(__file__).resolve().parents[3] / "fixtures" / "csv"


def _csv_fixtures() -> list[Path]:
    return sorted(_FIXTURES_CSV.glob("*.csv"))


def _is_valid(path: Path) -> bool:
    return path.stem.endswith("_valid")


def _is_invalid(path: Path) -> bool:
    return path.stem.endswith("_invalid")


class TestNonRegressionFixturesPipeline:
    """Parcourt toutes les fixtures CSV via inspect / validate / parse / preview.

    :spec: FEAT-013.1
    """

    def test_FEAT_013_1_fixtures_directory_populated(self) -> None:
        fixtures = _csv_fixtures()
        assert fixtures, f"aucune fixture CSV dans {_FIXTURES_CSV}"
        assert any(_is_valid(p) for p in fixtures)
        assert any(_is_invalid(p) for p in fixtures)
        assert (_FIXTURES_CSV / "unknown_format.csv").is_file()

    @pytest.mark.parametrize(
        "fixture_path",
        _csv_fixtures(),
        ids=lambda p: p.name,
    )
    def test_FEAT_013_1_pipeline_per_fixture(self, fixture_path: Path) -> None:
        use_case = ParseFileUseCase()
        name = fixture_path.name

        inspection = use_case.inspect(fixture_path)
        assert inspection.path == str(fixture_path) or inspection.file_name == name
        assert inspection.encoding
        assert inspection.separator

        validated = use_case.validate(fixture_path)
        parsed = use_case.parse(fixture_path)
        preview = use_case.preview(fixture_path, limit=5)

        assert validated.summary.status is parsed.summary.status
        assert validated.detected_type is parsed.detected_type
        assert preview.file_metadata.detected_type is parsed.detected_type

        fatal_codes = {
            e.issue.code
            for e in parsed.errors
            if e.issue.severity is ImportSeverity.FATAL
        }

        if name == "unknown_format.csv":
            assert parsed.detected_type is ImportFileType.UNKNOWN
            assert any(e.issue.code == "FILE_TYPE_UNKNOWN" for e in parsed.errors)
            assert not fatal_codes - {"FILE_TYPE_UNKNOWN"}
            return

        if _is_valid(fixture_path):
            assert ImportSeverity.FATAL not in {e.issue.severity for e in parsed.errors}
            assert parsed.detected_type is not ImportFileType.UNKNOWN
            assert parsed.summary.record_count >= 1 or parsed.warnings
            assert len(preview.records) <= 5
            assert len(preview.records) <= parsed.summary.record_count
            return

        if _is_invalid(fixture_path):
            assert parsed.errors, f"erreurs attendues pour {name}"
            assert parsed.detected_type is not ImportFileType.UNKNOWN
            return

        pytest.fail(f"fixture non classee (_valid/_invalid/unknown): {name}")
