"""Tests de AgentActivitiesLongReader."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from atpro.parser.readers.agent_activities_long_reader import AgentActivitiesLongReader

_LONG_HEADER = "Periode;Agent Groupe Agent;Noms de mesures;Valeurs de mesures"


class TestAgentActivitiesLongReader:
    def test_FEAT_009_1_multiple_measures_same_agent_day(self, tmp_path: Path) -> None:
        path = tmp_path / "activities_long.csv"
        path.write_text(
            _LONG_HEADER
            + "\n"
            + "15/06/2026;Alice DUPONT;Appels decroches;8\n"
            + "15/06/2026;Alice DUPONT;Appels recus;10\n"
            + "15/06/2026;Alice DUPONT;Temps login;01:00:00\n"
            + "15/06/2026;Alice DUPONT;Taux de decroches;80,00%\n",
            encoding="utf-8",
        )
        result = AgentActivitiesLongReader().read(path)
        assert not result.errors
        assert len(result.activities) == 1
        activity = result.activities[0]
        assert activity.activity_date == date(2026, 6, 15)
        assert activity.answered_calls == 8
        assert activity.received_calls == 10
        assert activity.login_time_seconds.seconds == 3600
        assert activity.answer_rate is not None
        assert activity.answer_rate.ratio == pytest.approx(0.8)

    def test_FEAT_009_1_unknown_measure(self, tmp_path: Path) -> None:
        path = tmp_path / "activities_unknown.csv"
        path.write_text(
            _LONG_HEADER
            + "\n"
            + "15/06/2026;Alice DUPONT;Appels decroches;5\n"
            + "15/06/2026;Alice DUPONT;Mesure Mystere;99\n",
            encoding="utf-8",
        )
        result = AgentActivitiesLongReader().read(path)
        assert not result.errors
        assert len(result.activities) == 1
        assert result.activities[0].answered_calls == 5
        assert result.activities[0].raw_metrics is not None
        assert "mesure_mystere" in result.activities[0].raw_metrics
        assert any(w.issue.code == "ACTIVITY_MEASURE_UNKNOWN" for w in result.warnings)

    def test_FEAT_009_1_duplicate_identical(self, tmp_path: Path) -> None:
        path = tmp_path / "activities_dup_ok.csv"
        path.write_text(
            _LONG_HEADER
            + "\n"
            + "15/06/2026;Alice DUPONT;Appels decroches;5\n"
            + "15/06/2026;Alice DUPONT;Appels decroches;5\n",
            encoding="utf-8",
        )
        result = AgentActivitiesLongReader().read(path)
        assert not result.errors
        assert len(result.activities) == 1
        assert result.activities[0].answered_calls == 5

    def test_FEAT_009_1_duplicate_contradictory(self, tmp_path: Path) -> None:
        path = tmp_path / "activities_dup_bad.csv"
        path.write_text(
            _LONG_HEADER
            + "\n"
            + "15/06/2026;Alice DUPONT;Appels decroches;5\n"
            + "15/06/2026;Alice DUPONT;Appels decroches;9\n",
            encoding="utf-8",
        )
        result = AgentActivitiesLongReader().read(path)
        assert any(e.issue.code == "ACTIVITY_MEASURE_CONFLICT" for e in result.errors)
        assert result.activities == ()

    def test_FEAT_009_1_schema_mismatch_warns(self) -> None:
        rows = [
            {
                "Periode": "15/06/2026",
                "Agent Groupe Agent": "Alice DUPONT",
                "Appels decroches": "1",
                "Appels recus": "2",
                "Temps login": "10",
                "Temps pret": "20",
            }
        ]
        result = AgentActivitiesLongReader().read_rows(rows)
        assert any(
            w.issue.code == "SCHEMA_NOT_ACTIVITIES_LONG" for w in result.warnings
        )

    def test_FEAT_009_1_unknown_schema_error(self, tmp_path: Path) -> None:
        path = tmp_path / "inconnu.csv"
        path.write_text("ColA;ColB\nx;y\n", encoding="utf-8")
        result = AgentActivitiesLongReader().read(path)
        assert any(
            e.issue.code == "SCHEMA_ACTIVITIES_LONG_REQUIRED" for e in result.errors
        )

    def test_FEAT_009_1_two_agents(self, tmp_path: Path) -> None:
        path = tmp_path / "activities_two.csv"
        path.write_text(
            _LONG_HEADER
            + "\n"
            + "15/06/2026;Alice DUPONT;Appels recus;10\n"
            + "15/06/2026;Bob MARTIN;Appels recus;3\n",
            encoding="utf-8",
        )
        result = AgentActivitiesLongReader().read(path)
        assert not result.errors
        assert len(result.activities) == 2
        by_name = {a.raw_agent_name: a for a in result.activities}
        assert by_name["Alice DUPONT"].received_calls == 10
        assert by_name["Bob MARTIN"].received_calls == 3
