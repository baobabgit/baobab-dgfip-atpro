"""Tests de CliOutcome."""

from __future__ import annotations

from atpro.interfaces.cli.cli_outcome import CliOutcome
from atpro.interfaces.cli.exit_code import ExitCode


class TestCliOutcome:
    def test_FEAT_002_5_frozen_fields(self) -> None:
        outcome = CliOutcome(exit_code=ExitCode.SUCCESS, text="ok")
        assert outcome.exit_code is ExitCode.SUCCESS
        assert outcome.text == "ok"
