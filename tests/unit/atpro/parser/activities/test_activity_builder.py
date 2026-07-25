"""Tests de ActivityBuilder."""

from __future__ import annotations

from datetime import date

from atpro.parser.activities.activity_builder import ActivityBuilder


class TestActivityBuilder:
    def test_FEAT_008_1_create_accumulator_french_date(self) -> None:
        builder = ActivityBuilder()
        acc, errors, _warnings = builder.create_accumulator(
            periode_raw="15 juin 2026",
            agent_raw="Jean-Pierre MARTIN",
            row_number=2,
        )
        assert not errors
        assert acc is not None
        assert acc.activity_date == date(2026, 6, 15)
        assert acc.raw_agent_name == "Jean-Pierre MARTIN"
        assert acc.agent_id is not None

    def test_FEAT_008_1_missing_periode_error(self) -> None:
        builder = ActivityBuilder()
        acc, errors, _ = builder.create_accumulator(
            periode_raw=None,
            agent_raw="Alice DUPONT",
            row_number=2,
        )
        assert acc is None
        assert any(e.issue.code == "ACTIVITY_DATE_REQUIRED" for e in errors)

    def test_FEAT_008_1_build_defaults(self) -> None:
        builder = ActivityBuilder()
        acc, errors, _ = builder.create_accumulator(
            periode_raw="15/06/2026",
            agent_raw="Alice DUPONT",
            row_number=2,
        )
        assert not errors and acc is not None
        result = builder.build([acc])
        assert len(result.activities) == 1
        activity = result.activities[0]
        assert activity.answered_calls == 0
        assert activity.login_time_seconds.seconds == 0
        assert activity.answer_rate is None

    def test_FEAT_008_1_invalid_date_and_empty_agent(self) -> None:
        builder = ActivityBuilder()
        acc1, errs1, _ = builder.create_accumulator(
            periode_raw="not-a-date",
            agent_raw="Alice DUPONT",
            row_number=2,
        )
        assert acc1 is None
        assert any(e.issue.code == "DATE_INVALID" for e in errs1)
        acc2, errs2, _ = builder.create_accumulator(
            periode_raw="15/06/2026",
            agent_raw="   ",
            row_number=3,
        )
        assert acc2 is None
        assert any(e.issue.code == "ACTIVITY_AGENT_REQUIRED" for e in errs2)

    def test_FEAT_008_1_apply_wide_already_normalized(self) -> None:
        builder = ActivityBuilder()
        acc, errors, _ = builder.create_accumulator(
            periode_raw="15/06/2026",
            agent_raw="Alice DUPONT",
            row_number=2,
        )
        assert not errors and acc is not None
        builder.apply_wide_row(
            acc,
            {"appels_decroches": "7", "periode": "15/06/2026"},
            row_number=2,
            already_normalized_keys=True,
        )
        result = builder.build([acc])
        assert result.activities[0].answered_calls == 7

    def test_FEAT_009_1_group_key_and_missing_measure(self) -> None:
        builder = ActivityBuilder()
        key = builder.group_key(periode_raw="15/06/2026", agent_raw="Alice DUPONT")
        assert key is not None
        assert key[0] == date(2026, 6, 15)
        assert builder.group_key(periode_raw="bad", agent_raw="Alice") is None
        acc, _, _ = builder.create_accumulator(
            periode_raw="15/06/2026",
            agent_raw="Alice DUPONT",
            row_number=2,
        )
        assert acc is not None
        builder.apply_long_measure(
            acc, measure_name=None, measure_value="1", row_number=2
        )
        assert any(w.issue.code == "ACTIVITY_MEASURE_MISSING" for w in acc.warnings)
