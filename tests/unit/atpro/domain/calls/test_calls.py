"""Tests des modeles appels."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from atpro.domain.calls import Call, CallSegment
from atpro.domain.enums import CallDirection
from atpro.domain.exceptions import DomainError
from atpro.domain.value_objects import DurationSeconds


class TestCall:
    """Instanciation Call."""

    def test_FEAT_005_1_instantiate_call(self) -> None:
        now = datetime(2026, 1, 1, 10, 0, tzinfo=UTC)
        call = Call(
            id="c1",
            source_system="atpro",
            external_call_id="EXT-1",
            direction=CallDirection.INCOMING,
            started_at=now,
            ended_at=now,
            caller_hash="h1",
            callee_hash="h2",
            flow="standard",
            service="accueil",
            global_result="ok",
            source_import_batch_id="b1",
            created_at=now,
            updated_at=now,
        )
        assert call.direction is CallDirection.INCOMING

    def test_FEAT_005_1_call_requires_external_id(self) -> None:
        now = datetime(2026, 1, 1, tzinfo=UTC)
        with pytest.raises(DomainError):
            Call(
                id="c1",
                source_system="atpro",
                external_call_id=" ",
                direction=CallDirection.OUTGOING,
                started_at=now,
                ended_at=None,
                caller_hash=None,
                callee_hash=None,
                flow=None,
                service=None,
                global_result=None,
                source_import_batch_id=None,
                created_at=now,
                updated_at=now,
            )
        with pytest.raises(DomainError):
            Call(
                id=" ",
                source_system="atpro",
                external_call_id="EXT",
                direction=CallDirection.OUTGOING,
                started_at=now,
                ended_at=None,
                caller_hash=None,
                callee_hash=None,
                flow=None,
                service=None,
                global_result=None,
                source_import_batch_id=None,
                created_at=now,
                updated_at=now,
            )
        with pytest.raises(DomainError):
            Call(
                id="c1",
                source_system=" ",
                external_call_id="EXT",
                direction=CallDirection.OUTGOING,
                started_at=now,
                ended_at=None,
                caller_hash=None,
                callee_hash=None,
                flow=None,
                service=None,
                global_result=None,
                source_import_batch_id=None,
                created_at=now,
                updated_at=now,
            )


class TestCallSegment:
    """Instanciation CallSegment."""

    def test_FEAT_005_1_instantiate_segment(self) -> None:
        now = datetime(2026, 1, 1, tzinfo=UTC)
        segment = CallSegment(
            id="cs1",
            call_id="c1",
            segment_index=0,
            agent_id=None,
            raw_agent_name="Agent X",
            site_id=None,
            started_at=now,
            ended_at=now,
            talk_duration_seconds=DurationSeconds.from_seconds(30),
            hold_duration_seconds=DurationSeconds.from_seconds(5),
            qualification_category=None,
            qualification_reason=None,
            hangup_origin=None,
            source_row_numbers=(2, 3),
            line_fingerprint="fp",
            created_at=now,
        )
        assert segment.source_row_numbers == (2, 3)

    def test_FEAT_005_1_segment_index_negative(self) -> None:
        now = datetime(2026, 1, 1, tzinfo=UTC)
        with pytest.raises(DomainError):
            CallSegment(
                id="cs1",
                call_id="c1",
                segment_index=-1,
                agent_id=None,
                raw_agent_name="Agent X",
                site_id=None,
                started_at=now,
                ended_at=None,
                talk_duration_seconds=DurationSeconds.from_seconds(0),
                hold_duration_seconds=DurationSeconds.from_seconds(0),
                qualification_category=None,
                qualification_reason=None,
                hangup_origin=None,
                source_row_numbers=(),
                line_fingerprint=None,
                created_at=now,
            )
        with pytest.raises(DomainError):
            CallSegment(
                id=" ",
                call_id="c1",
                segment_index=0,
                agent_id=None,
                raw_agent_name="Agent X",
                site_id=None,
                started_at=now,
                ended_at=None,
                talk_duration_seconds=DurationSeconds.from_seconds(0),
                hold_duration_seconds=DurationSeconds.from_seconds(0),
                qualification_category=None,
                qualification_reason=None,
                hangup_origin=None,
                source_row_numbers=(),
                line_fingerprint=None,
                created_at=now,
            )
        with pytest.raises(DomainError):
            CallSegment(
                id="cs1",
                call_id=" ",
                segment_index=0,
                agent_id=None,
                raw_agent_name="Agent X",
                site_id=None,
                started_at=now,
                ended_at=None,
                talk_duration_seconds=DurationSeconds.from_seconds(0),
                hold_duration_seconds=DurationSeconds.from_seconds(0),
                qualification_category=None,
                qualification_reason=None,
                hangup_origin=None,
                source_row_numbers=(),
                line_fingerprint=None,
                created_at=now,
            )
