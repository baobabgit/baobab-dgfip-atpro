"""Tests d'integration CLI via Typer CliRunner."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from atpro.interfaces.cli.app import app
from atpro.interfaces.cli.exit_code import ExitCode

_INCOMING_HEADER = (
    "ID de l'appel;Numero appelant;Numero appele;Nom de l'agent;"
    "Debut d'appel;Fin d'appel;Flux;Service;Noms de mesures;Valeurs de mesures"
)

_INCOMING_ROW = (
    "A1;0611111111;0142000000;Alice DUPONT;"
    "15/06/2026 10:00:00;15/06/2026 10:05:00;F1;S1;"
    "Duree de communication;120"
)


def _write_incoming(tmp_path: Path) -> Path:
    path = tmp_path / "appels_entrants.csv"
    path.write_text(_INCOMING_HEADER + "\n" + _INCOMING_ROW + "\n", encoding="utf-8")
    return path


def _write_unknown(tmp_path: Path) -> Path:
    path = tmp_path / "garbage.csv"
    path.write_text("foo;bar;baz\n1;2;3\n", encoding="utf-8")
    return path


class TestApp:
    def test_FEAT_002_5_inspect_success(self, tmp_path: Path) -> None:
        path = _write_incoming(tmp_path)
        result = CliRunner().invoke(app, ["file", "inspect", str(path)])
        assert result.exit_code == int(ExitCode.SUCCESS)
        assert "detected_type:" in result.stdout
        assert "incoming_calls" in result.stdout

    def test_FEAT_002_5_validate_success(self, tmp_path: Path) -> None:
        path = _write_incoming(tmp_path)
        result = CliRunner().invoke(app, ["file", "validate", str(path)])
        assert result.exit_code == int(ExitCode.SUCCESS)
        assert "status: success" in result.stdout

    def test_FEAT_002_5_preview_success(self, tmp_path: Path) -> None:
        path = _write_incoming(tmp_path)
        result = CliRunner().invoke(app, ["file", "preview", str(path), "--limit", "5"])
        assert result.exit_code == int(ExitCode.SUCCESS)
        assert "preview_records:" in result.stdout
        assert "limit: 5" in result.stdout

    def test_FEAT_002_5_missing_file_exit_2(self, tmp_path: Path) -> None:
        missing = tmp_path / "absent.csv"
        result = CliRunner().invoke(app, ["file", "inspect", str(missing)])
        assert result.exit_code == int(ExitCode.MISSING_OR_UNREADABLE)
        assert "FILE_ABSENT" in result.stdout

    def test_FEAT_002_5_unknown_format_exit_3(self, tmp_path: Path) -> None:
        path = _write_unknown(tmp_path)
        result = CliRunner().invoke(app, ["file", "validate", str(path)])
        assert result.exit_code == int(ExitCode.UNKNOWN_FORMAT)

    def test_FEAT_002_5_json_output_valid(self, tmp_path: Path) -> None:
        path = _write_incoming(tmp_path)
        runner = CliRunner()
        inspect_result = runner.invoke(app, ["file", "inspect", str(path), "--json"])
        validate_result = runner.invoke(app, ["file", "validate", str(path), "--json"])
        preview_result = runner.invoke(
            app, ["file", "preview", str(path), "--json", "--limit", "2"]
        )
        assert inspect_result.exit_code == int(ExitCode.SUCCESS)
        assert validate_result.exit_code == int(ExitCode.SUCCESS)
        assert preview_result.exit_code == int(ExitCode.SUCCESS)
        inspect_payload = json.loads(inspect_result.stdout)
        validate_payload = json.loads(validate_result.stdout)
        preview_payload = json.loads(preview_result.stdout)
        assert inspect_payload["detected_type"] == "incoming_calls"
        assert validate_payload["summary"]["status"] == "success"
        assert preview_payload["limit"] == 2
