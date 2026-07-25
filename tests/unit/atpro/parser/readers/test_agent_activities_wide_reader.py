"""Tests de AgentActivitiesWideReader."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from atpro.parser.readers.agent_activities_wide_reader import AgentActivitiesWideReader

_WIDE_HEADER = (
    "Periode;Agent Groupe Agent;Appels decroches;Appels recus;"
    "Temps login;Temps pret;Taux de decroches;Temps telephone"
)


class TestAgentActivitiesWideReader:
    def test_FEAT_008_1_complete_line(self, tmp_path: Path) -> None:
        path = tmp_path / "activities_wide.csv"
        path.write_text(
            _WIDE_HEADER
            + "\n"
            + "15/06/2026;Alice DUPONT;8;10;01:00:00;00:45:00;80,00%;00:30:00\n",
            encoding="utf-8",
        )
        result = AgentActivitiesWideReader().read(path)
        assert not result.errors
        assert len(result.activities) == 1
        activity = result.activities[0]
        assert activity.activity_date == date(2026, 6, 15)
        assert activity.answered_calls == 8
        assert activity.received_calls == 10
        assert activity.login_time_seconds.seconds == 3600
        assert activity.ready_time_seconds.seconds == 2700
        assert activity.phone_time_seconds.seconds == 1800
        assert activity.answer_rate is not None
        assert activity.answer_rate.ratio == pytest.approx(0.8)
        assert activity.raw_agent_name == "Alice DUPONT"

    def test_FEAT_008_1_empty_values(self, tmp_path: Path) -> None:
        path = tmp_path / "activities_empty.csv"
        path.write_text(
            _WIDE_HEADER + "\n" + "15/06/2026;Bob MARTIN;;;;;\n",
            encoding="utf-8",
        )
        result = AgentActivitiesWideReader().read(path)
        assert not result.errors
        assert len(result.activities) == 1
        activity = result.activities[0]
        assert activity.answered_calls == 0
        assert activity.received_calls == 0
        assert activity.login_time_seconds.seconds == 0
        assert activity.ready_time_seconds.seconds == 0
        assert activity.answer_rate is None

    def test_FEAT_008_1_percent_with_comma(self, tmp_path: Path) -> None:
        path = tmp_path / "activities_pct.csv"
        path.write_text(
            _WIDE_HEADER + "\n" + "15/06/2026;Alice DUPONT;5;5;100;100;12,5%;\n",
            encoding="utf-8",
        )
        result = AgentActivitiesWideReader().read(path)
        assert not result.errors
        assert result.activities[0].answer_rate is not None
        assert result.activities[0].answer_rate.ratio == pytest.approx(0.125)

    def test_FEAT_008_1_french_date(self, tmp_path: Path) -> None:
        path = tmp_path / "activities_fr_date.csv"
        path.write_text(
            _WIDE_HEADER + "\n" + "15 juin 2026;Alice DUPONT;1;2;10;20;50,00%;\n",
            encoding="utf-8",
        )
        result = AgentActivitiesWideReader().read(path)
        assert not result.errors
        assert result.activities[0].activity_date == date(2026, 6, 15)

    def test_FEAT_008_1_compound_agent_name(self, tmp_path: Path) -> None:
        path = tmp_path / "activities_compound.csv"
        path.write_text(
            _WIDE_HEADER + "\n" + "15/06/2026;Jean-Pierre MARTIN;3;4;30;40;75,00%;\n",
            encoding="utf-8",
        )
        result = AgentActivitiesWideReader().read(path)
        assert not result.errors
        activity = result.activities[0]
        assert activity.raw_agent_name == "Jean-Pierre MARTIN"
        assert activity.agent_id is not None
        assert "jean-pierre" in activity.agent_id

    def test_FEAT_008_1_schema_extra_columns_warn(self, tmp_path: Path) -> None:
        path = tmp_path / "activites_agents.csv"
        path.write_text(
            _WIDE_HEADER + "\n" + "15/06/2026;Alice DUPONT;1;2;10;20;50,00%;30\n",
            encoding="utf-8",
        )
        result = AgentActivitiesWideReader().read(path)
        assert not result.errors
        assert any(w.issue.code == "SCHEMA_EXTRA_COLUMNS" for w in result.warnings)

    def test_FEAT_008_1_unknown_schema_error(self, tmp_path: Path) -> None:
        path = tmp_path / "inconnu.csv"
        path.write_text("ColA;ColB\nx;y\n", encoding="utf-8")
        result = AgentActivitiesWideReader().read(path)
        assert any(
            e.issue.code == "SCHEMA_ACTIVITIES_WIDE_REQUIRED" for e in result.errors
        )

    def test_FEAT_008_1_read_rows_helper(self) -> None:
        rows = [
            {
                "Periode": "16/06/2026",
                "Agent Groupe Agent": "Alice DUPONT",
                "Appels decroches": "2",
                "Appels recus": "3",
                "Temps login": "60",
                "Temps pret": "40",
            }
        ]
        result = AgentActivitiesWideReader().read_rows(rows)
        assert len(result.activities) == 1
        assert result.activities[0].answered_calls == 2

    def test_FEAT_008_1_non_activities_schema_warns(self) -> None:
        rows = [
            {
                "Numero Ticket": "T1",
                "Date-Heure Creation Ticket": "15/06/2026 10:00:00",
                "Statut Ticket": "Ouvert",
                "Site Repartition Ticket": "Site A",
            }
        ]
        result = AgentActivitiesWideReader().read_rows(rows)
        assert any(w.issue.code == "SCHEMA_NOT_ACTIVITIES" for w in result.warnings)

    def test_FEAT_008_1_long_schema_warns_not_wide(self) -> None:
        rows = [
            {
                "Periode": "15/06/2026",
                "Agent Groupe Agent": "Alice DUPONT",
                "Noms de mesures": "Appels decroches",
                "Valeurs de mesures": "1",
            }
        ]
        result = AgentActivitiesWideReader().read_rows(rows)
        assert any(
            w.issue.code == "SCHEMA_NOT_ACTIVITIES_WIDE" for w in result.warnings
        )
