"""Tests de ActivityAccumulator."""

from __future__ import annotations

from datetime import date

from atpro.domain.value_objects.duration_seconds import DurationSeconds
from atpro.parser.activities.activity_accumulator import ActivityAccumulator


class TestActivityAccumulator:
    def test_FEAT_009_1_duplicate_identical_ok(self) -> None:
        acc = ActivityAccumulator(
            activity_date=date(2026, 6, 15),
            raw_agent_name="Alice DUPONT",
            agent_id="agent:alice dupont",
        )
        acc.add_measure("appels_decroches", "10", row_number=2, column="valeurs")
        acc.add_measure("appels_decroches", "10", row_number=3, column="valeurs")
        assert not acc.errors
        assert acc.count_value("answered_calls") == 10

    def test_FEAT_009_1_duplicate_contradictory(self) -> None:
        acc = ActivityAccumulator(
            activity_date=date(2026, 6, 15),
            raw_agent_name="Alice DUPONT",
            agent_id="agent:alice dupont",
        )
        acc.add_measure("appels_decroches", "10", row_number=2, column="valeurs")
        acc.add_measure("appels_decroches", "12", row_number=3, column="valeurs")
        assert any(e.issue.code == "ACTIVITY_MEASURE_CONFLICT" for e in acc.errors)
        assert acc.has_blocking_errors

    def test_FEAT_009_1_unknown_measure(self) -> None:
        acc = ActivityAccumulator(
            activity_date=date(2026, 6, 15),
            raw_agent_name="Alice DUPONT",
            agent_id="agent:alice dupont",
        )
        acc.add_measure("mesure_custom", "42", row_number=2, column="noms")
        assert acc.raw_metrics["mesure_custom"] == "42"
        assert any(w.issue.code == "ACTIVITY_MEASURE_UNKNOWN" for w in acc.warnings)

    def test_FEAT_008_1_empty_defaults(self) -> None:
        acc = ActivityAccumulator(
            activity_date=date(2026, 6, 15),
            raw_agent_name="Alice DUPONT",
            agent_id="agent:alice dupont",
        )
        acc.add_measure("appels_recus", "", row_number=2, column="appels_recus")
        acc.add_measure("temps_login", "", row_number=2, column="temps_login")
        acc.add_measure("taux_de_decroches", "", row_number=2, column="taux")
        assert acc.count_value("received_calls") == 0
        assert acc.duration_value("login_time_seconds") == DurationSeconds.from_seconds(
            0
        )
        assert acc.percent_value("answer_rate") is None

    def test_FEAT_008_1_invalid_count_and_duration(self) -> None:
        acc = ActivityAccumulator(
            activity_date=date(2026, 6, 15),
            raw_agent_name="Alice DUPONT",
            agent_id="agent:alice dupont",
        )
        acc.add_measure("appels_recus", "x", row_number=2, column="appels_recus")
        acc.add_measure("temps_login", "nope", row_number=2, column="temps_login")
        acc.add_measure("taux_de_decroches", "n/a", row_number=2, column="taux")
        assert any(e.issue.code == "ACTIVITY_COUNT_INVALID" for e in acc.errors)
        assert any(e.issue.code == "DURATION_INVALID" for e in acc.errors)
        assert any(e.issue.code == "PERCENTAGE_INVALID" for e in acc.errors)

    def test_FEAT_009_1_unknown_measure_conflict(self) -> None:
        acc = ActivityAccumulator(
            activity_date=date(2026, 6, 15),
            raw_agent_name="Alice DUPONT",
            agent_id="agent:alice dupont",
        )
        acc.add_measure("custom", "1", row_number=2, column="noms")
        acc.add_measure("custom", "2", row_number=3, column="noms")
        assert any(e.issue.code == "ACTIVITY_MEASURE_CONFLICT" for e in acc.errors)
