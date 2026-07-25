"""Tests de consolidation des appels."""

from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from atpro.domain.enums.call_direction import CallDirection
from atpro.parser.calls.call_consolidator import CallConsolidator
from atpro.parser.calls.raw_call_row import RawCallRow

_PARIS = ZoneInfo("Europe/Paris")


def _row(
    row_number: int,
    *,
    call_id: str = "A1",
    agent: str = "Alice DUPONT",
    start: str = "15/06/2026 10:00:00",
    end: str = "15/06/2026 10:05:00",
    measure: str | None = "Duree de communication",
    value: str | None = "120",
    caller: str | None = "0611111111",
    callee: str | None = "0142000000",
    flow: str | None = "Flux1",
    service: str | None = "Svc1",
) -> RawCallRow:
    return RawCallRow(
        row_number=row_number,
        external_call_id=call_id,
        caller=caller,
        callee=callee,
        agent_name=agent,
        started_at_raw=start,
        ended_at_raw=end,
        flow=flow,
        service=service,
        measure_name=measure,
        measure_value=value,
    )


class TestCallConsolidator:
    def test_FEAT_005_4_two_measure_lines_one_segment(self) -> None:
        result = CallConsolidator().consolidate(
            [
                _row(2, measure="Duree de communication", value="120"),
                _row(3, measure="Duree de mise en garde", value="30"),
            ],
            direction=CallDirection.INCOMING,
            now=datetime(2026, 6, 15, 12, 0, tzinfo=_PARIS),
        )
        assert len(result.errors) == 0
        assert len(result.calls) == 1
        assert len(result.segments) == 1
        assert result.segments[0].talk_duration_seconds.seconds == 120
        assert result.segments[0].hold_duration_seconds.seconds == 30
        assert result.segments[0].source_row_numbers == (2, 3)
        assert result.calls[0].direction is CallDirection.INCOMING
        assert result.calls[0].caller_hash is not None

    def test_FEAT_005_4_contradictory_measure(self) -> None:
        result = CallConsolidator().consolidate(
            [
                _row(2, measure="Duree de communication", value="120"),
                _row(3, measure="Duree de communication", value="90"),
            ],
            direction=CallDirection.INCOMING,
        )
        assert any(e.issue.code == "CALL_MEASURE_CONFLICT" for e in result.errors)
        assert result.segments == ()

    def test_FEAT_005_4_multi_segments(self) -> None:
        result = CallConsolidator().consolidate(
            [
                _row(2, agent="Alice DUPONT", value="60"),
                _row(3, agent="Bob MARTIN", value="40"),
            ],
            direction=CallDirection.INCOMING,
        )
        assert len(result.calls) == 1
        assert len(result.segments) == 2
        assert any(w.issue.code == "CALL_MULTI_SEGMENT" for w in result.warnings)

    def test_FEAT_005_4_invalid_row_missing_call_id(self) -> None:
        result = CallConsolidator().consolidate(
            [
                RawCallRow(
                    row_number=2,
                    external_call_id=None,
                    caller=None,
                    callee="0142",
                    agent_name="Alice",
                    started_at_raw="15/06/2026 10:00:00",
                    ended_at_raw="15/06/2026 10:01:00",
                    flow=None,
                    service=None,
                    measure_name="Duree de communication",
                    measure_value="10",
                )
            ],
            direction=CallDirection.OUTGOING,
        )
        assert any(e.issue.code == "CALL_ID_MISSING" for e in result.errors)
        assert result.calls == ()

    def test_FEAT_005_4_unknown_measure_warning(self) -> None:
        result = CallConsolidator().consolidate(
            [
                _row(2, measure="Duree de communication", value="10"),
                _row(3, measure="Mesure fantome", value="1"),
            ],
            direction=CallDirection.INCOMING,
        )
        assert len(result.segments) == 1
        assert any(w.issue.code == "CALL_MEASURE_UNKNOWN" for w in result.warnings)

    def test_FEAT_005_4_end_before_start(self) -> None:
        result = CallConsolidator().consolidate(
            [
                _row(
                    2,
                    start="15/06/2026 11:00:00",
                    end="15/06/2026 10:00:00",
                    value="10",
                )
            ],
            direction=CallDirection.INCOMING,
        )
        assert any(e.issue.code == "CALL_END_BEFORE_START" for e in result.errors)

    def test_FEAT_005_4_empty_agent_warning(self) -> None:
        result = CallConsolidator().consolidate(
            [_row(2, agent="", value="10")],
            direction=CallDirection.INCOMING,
        )
        assert any(w.issue.code == "CALL_AGENT_EMPTY" for w in result.warnings)
        assert len(result.segments) == 1

    def test_FEAT_005_4_invalid_start_date(self) -> None:
        result = CallConsolidator().consolidate(
            [_row(2, start="pas-une-date", value="10")],
            direction=CallDirection.INCOMING,
        )
        assert any(e.issue.code == "DATE_INVALID" for e in result.errors)
