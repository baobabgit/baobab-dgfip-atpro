"""Non-regression : CLI ``atpro file`` sur fixtures cles.

:spec: FEAT-013.1
"""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from atpro.interfaces.cli.app import app
from atpro.interfaces.cli.exit_code import ExitCode

_FIXTURES_CSV = Path(__file__).resolve().parents[3] / "fixtures" / "csv"
_runner = CliRunner()


def _fixture(name: str) -> Path:
    return _FIXTURES_CSV / name


class TestNonRegressionCli:
    """Codes de sortie CLI stables sur fixtures representatifs.

    :spec: FEAT-013.1
    """

    def test_FEAT_013_1_inspect_valid_exit_0(self) -> None:
        result = _runner.invoke(
            app, ["file", "inspect", str(_fixture("incoming_calls_valid.csv"))]
        )
        assert result.exit_code == int(ExitCode.SUCCESS)
        assert "incoming_calls" in result.stdout.lower() or result.stdout

    def test_FEAT_013_1_validate_valid_exit_0(self) -> None:
        result = _runner.invoke(
            app, ["file", "validate", str(_fixture("tickets_long_valid.csv"))]
        )
        assert result.exit_code == int(ExitCode.SUCCESS)

    def test_FEAT_013_1_preview_valid_exit_0(self) -> None:
        result = _runner.invoke(
            app,
            [
                "file",
                "preview",
                str(_fixture("outgoing_calls_valid.csv")),
                "--limit",
                "3",
            ],
        )
        assert result.exit_code == int(ExitCode.SUCCESS)

    def test_FEAT_013_1_validate_invalid_exit_1(self) -> None:
        result = _runner.invoke(
            app, ["file", "validate", str(_fixture("tickets_invalid.csv"))]
        )
        assert result.exit_code == int(ExitCode.INVALID_FILE)

    def test_FEAT_013_1_preview_invalid_exit_1(self) -> None:
        result = _runner.invoke(
            app, ["file", "preview", str(_fixture("incoming_calls_invalid.csv"))]
        )
        assert result.exit_code == int(ExitCode.INVALID_FILE)

    def test_FEAT_013_1_validate_missing_exit_2(self, tmp_path: Path) -> None:
        missing = tmp_path / "absent_non_regression.csv"
        result = _runner.invoke(app, ["file", "validate", str(missing)])
        assert result.exit_code == int(ExitCode.MISSING_OR_UNREADABLE)

    def test_FEAT_013_1_inspect_missing_exit_2(self, tmp_path: Path) -> None:
        missing = tmp_path / "absent_inspect.csv"
        result = _runner.invoke(app, ["file", "inspect", str(missing)])
        assert result.exit_code == int(ExitCode.MISSING_OR_UNREADABLE)

    def test_FEAT_013_1_validate_unknown_exit_3(self) -> None:
        result = _runner.invoke(
            app, ["file", "validate", str(_fixture("unknown_format.csv"))]
        )
        assert result.exit_code == int(ExitCode.UNKNOWN_FORMAT)

    def test_FEAT_013_1_preview_unknown_exit_3(self) -> None:
        result = _runner.invoke(
            app, ["file", "preview", str(_fixture("unknown_format.csv"))]
        )
        assert result.exit_code == int(ExitCode.UNKNOWN_FORMAT)

    def test_FEAT_013_1_inspect_unknown_still_succeeds(self) -> None:
        """Inspect detecte le format sans echec fatal de lecture."""
        result = _runner.invoke(
            app, ["file", "inspect", str(_fixture("unknown_format.csv"))]
        )
        assert result.exit_code == int(ExitCode.SUCCESS)

    def test_FEAT_013_1_activities_valid_validate_exit_0(self) -> None:
        result = _runner.invoke(
            app, ["file", "validate", str(_fixture("activities_wide_valid.csv"))]
        )
        assert result.exit_code == int(ExitCode.SUCCESS)
