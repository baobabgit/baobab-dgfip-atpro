"""Tests de file_commands et point d'entree."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from atpro.interfaces.cli import file_commands
from atpro.interfaces.cli.app import run
from atpro.interfaces.cli.cli_outcome import CliOutcome
from atpro.interfaces.cli.exit_code import ExitCode
from atpro.interfaces.cli.file_cli_service import FileCliService


class TestFileCommands:
    def test_FEAT_002_5_configure_service_and_empty_text(self) -> None:
        service = MagicMock(spec=FileCliService)
        service.inspect.return_value = CliOutcome(exit_code=ExitCode.SUCCESS, text="")
        file_commands.configure_service(service)
        try:
            result = CliRunner().invoke(
                file_commands.file_app, ["inspect", "dummy.csv"]
            )
            assert result.exit_code == int(ExitCode.SUCCESS)
            assert result.stdout == ""
            service.inspect.assert_called_once()
        finally:
            file_commands.configure_service(FileCliService())

    def test_FEAT_002_5_run_invokes_app(self) -> None:
        with patch("atpro.interfaces.cli.app.app") as mock_app:
            run()
            mock_app.assert_called_once_with()
