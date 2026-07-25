"""Tests du modele AgentDailyActivity."""

from __future__ import annotations

from datetime import UTC, date, datetime

import pytest

from atpro.domain.activities import AgentDailyActivity
from atpro.domain.exceptions import DomainError
from atpro.domain.value_objects import DurationSeconds, Percentage


def _zero() -> DurationSeconds:
    return DurationSeconds.from_seconds(0)


class TestAgentDailyActivity:
    """Instanciation AgentDailyActivity."""

    def test_FEAT_005_1_instantiate_activity(self) -> None:
        now = datetime(2026, 1, 1, tzinfo=UTC)
        activity = AgentDailyActivity(
            id="act1",
            agent_id="a1",
            raw_agent_name="Agent X",
            site_id="s1",
            activity_date=date(2026, 1, 1),
            received_calls=10,
            answered_calls=8,
            outgoing_calls=2,
            transferred_in_calls=1,
            handled_calls_total=9,
            transferred_calls=1,
            hold_count=0,
            consultation_count=0,
            login_time_seconds=_zero(),
            ready_time_seconds=_zero(),
            not_ready_time_seconds=_zero(),
            phone_time_seconds=_zero(),
            incoming_talk_time_seconds=_zero(),
            outgoing_talk_time_seconds=_zero(),
            after_call_work_seconds=_zero(),
            rona_time_seconds=_zero(),
            hold_duration_seconds=_zero(),
            answer_rate=Percentage.from_ratio(0.8),
            hold_rate=None,
            raw_metrics={"custom": 1},
            source_import_batch_id="b1",
            line_fingerprint="fp",
            created_at=now,
        )
        assert activity.answered_calls == 8

    def test_FEAT_005_1_activity_rejects_negative_counts(self) -> None:
        now = datetime(2026, 1, 1, tzinfo=UTC)
        with pytest.raises(DomainError):
            AgentDailyActivity(
                id="act1",
                agent_id=None,
                raw_agent_name="Agent X",
                site_id=None,
                activity_date=date(2026, 1, 1),
                received_calls=-1,
                answered_calls=0,
                outgoing_calls=0,
                transferred_in_calls=0,
                handled_calls_total=0,
                transferred_calls=0,
                hold_count=0,
                consultation_count=0,
                login_time_seconds=_zero(),
                ready_time_seconds=_zero(),
                not_ready_time_seconds=_zero(),
                phone_time_seconds=_zero(),
                incoming_talk_time_seconds=_zero(),
                outgoing_talk_time_seconds=_zero(),
                after_call_work_seconds=_zero(),
                rona_time_seconds=_zero(),
                hold_duration_seconds=_zero(),
                answer_rate=None,
                hold_rate=None,
                raw_metrics=None,
                source_import_batch_id=None,
                line_fingerprint=None,
                created_at=now,
            )
        with pytest.raises(DomainError):
            AgentDailyActivity(
                id=" ",
                agent_id=None,
                raw_agent_name="Agent X",
                site_id=None,
                activity_date=date(2026, 1, 1),
                received_calls=0,
                answered_calls=0,
                outgoing_calls=0,
                transferred_in_calls=0,
                handled_calls_total=0,
                transferred_calls=0,
                hold_count=0,
                consultation_count=0,
                login_time_seconds=_zero(),
                ready_time_seconds=_zero(),
                not_ready_time_seconds=_zero(),
                phone_time_seconds=_zero(),
                incoming_talk_time_seconds=_zero(),
                outgoing_talk_time_seconds=_zero(),
                after_call_work_seconds=_zero(),
                rona_time_seconds=_zero(),
                hold_duration_seconds=_zero(),
                answer_rate=None,
                hold_rate=None,
                raw_metrics=None,
                source_import_batch_id=None,
                line_fingerprint=None,
                created_at=now,
            )
        with pytest.raises(DomainError):
            AgentDailyActivity(
                id="act1",
                agent_id=None,
                raw_agent_name=" ",
                site_id=None,
                activity_date=date(2026, 1, 1),
                received_calls=0,
                answered_calls=0,
                outgoing_calls=0,
                transferred_in_calls=0,
                handled_calls_total=0,
                transferred_calls=0,
                hold_count=0,
                consultation_count=0,
                login_time_seconds=_zero(),
                ready_time_seconds=_zero(),
                not_ready_time_seconds=_zero(),
                phone_time_seconds=_zero(),
                incoming_talk_time_seconds=_zero(),
                outgoing_talk_time_seconds=_zero(),
                after_call_work_seconds=_zero(),
                rona_time_seconds=_zero(),
                hold_duration_seconds=_zero(),
                answer_rate=None,
                hold_rate=None,
                raw_metrics=None,
                source_import_batch_id=None,
                line_fingerprint=None,
                created_at=now,
            )
