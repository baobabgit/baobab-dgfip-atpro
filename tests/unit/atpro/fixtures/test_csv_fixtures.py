"""Tests des fixtures CSV anonymisees (FEAT-012.1)."""

from __future__ import annotations

from pathlib import Path

from atpro.domain.enums.call_direction import CallDirection
from atpro.domain.enums.import_file_type import ImportFileType
from atpro.parser.parse_file_use_case import ParseFileUseCase
from atpro.parser.readers.agent_activities_long_reader import AgentActivitiesLongReader
from atpro.parser.readers.agent_activities_wide_reader import AgentActivitiesWideReader
from atpro.parser.readers.incoming_calls_reader import IncomingCallsReader
from atpro.parser.readers.outgoing_calls_reader import OutgoingCallsReader
from atpro.parser.readers.tickets_reader import TicketsReader

_FIXTURES_CSV = Path(__file__).resolve().parents[3] / "fixtures" / "csv"


def _fixture(name: str) -> Path:
    return _FIXTURES_CSV / name


class TestCsvFixtures:
    """Validation des fixtures anonymisees versionnees.

    :spec: FEAT-012.1
    """

    def test_FEAT_012_1_incoming_calls_valid(self) -> None:
        result = IncomingCallsReader().read(_fixture("incoming_calls_valid.csv"))
        assert not result.errors
        assert len(result.calls) >= 1
        assert result.calls[0].direction is CallDirection.INCOMING

    def test_FEAT_012_1_incoming_calls_invalid(self) -> None:
        result = IncomingCallsReader().read(_fixture("incoming_calls_invalid.csv"))
        assert any(e.issue.code == "CALL_END_BEFORE_START" for e in result.errors)

    def test_FEAT_012_1_outgoing_calls_valid(self) -> None:
        result = OutgoingCallsReader().read(_fixture("outgoing_calls_valid.csv"))
        assert not result.errors
        assert len(result.calls) >= 1
        assert result.calls[0].direction is CallDirection.OUTGOING

    def test_FEAT_012_1_outgoing_calls_invalid(self) -> None:
        result = OutgoingCallsReader().read(_fixture("outgoing_calls_invalid.csv"))
        assert any(e.issue.code == "CALL_END_BEFORE_START" for e in result.errors)

    def test_FEAT_012_1_tickets_long_valid(self) -> None:
        result = TicketsReader().read(_fixture("tickets_long_valid.csv"))
        assert not result.errors
        assert len(result.tickets) >= 1

    def test_FEAT_012_1_tickets_short_valid(self) -> None:
        result = TicketsReader().read(_fixture("tickets_short_valid.csv"))
        assert not result.errors
        assert len(result.tickets) >= 1

    def test_FEAT_012_1_tickets_invalid(self) -> None:
        result = TicketsReader().read(_fixture("tickets_invalid.csv"))
        assert any(
            e.issue.code == "TICKET_RESOLVED_BEFORE_CREATED" for e in result.errors
        )

    def test_FEAT_012_1_activities_wide_valid(self) -> None:
        result = AgentActivitiesWideReader().read(_fixture("activities_wide_valid.csv"))
        assert not result.errors
        assert len(result.activities) >= 1

    def test_FEAT_012_1_activities_long_valid(self) -> None:
        result = AgentActivitiesLongReader().read(_fixture("activities_long_valid.csv"))
        assert not result.errors
        assert len(result.activities) >= 1

    def test_FEAT_012_1_activities_invalid(self) -> None:
        result = AgentActivitiesLongReader().read(_fixture("activities_invalid.csv"))
        assert any(e.issue.code == "ACTIVITY_MEASURE_CONFLICT" for e in result.errors)

    def test_FEAT_012_1_unknown_format_via_parse(self) -> None:
        result = ParseFileUseCase().parse(_fixture("unknown_format.csv"))
        assert result.detected_type is ImportFileType.UNKNOWN
        assert any(e.issue.code == "FILE_TYPE_UNKNOWN" for e in result.errors)

    def test_FEAT_012_1_parse_valid_incoming_no_blocking_errors(self) -> None:
        result = ParseFileUseCase().parse(_fixture("incoming_calls_valid.csv"))
        assert not result.errors
        assert result.detected_type is ImportFileType.INCOMING_CALLS
        assert result.summary.record_count >= 1

    def test_FEAT_012_1_all_required_fixtures_exist(self) -> None:
        required = (
            "incoming_calls_valid.csv",
            "incoming_calls_invalid.csv",
            "outgoing_calls_valid.csv",
            "tickets_long_valid.csv",
            "tickets_short_valid.csv",
            "activities_wide_valid.csv",
            "activities_long_valid.csv",
            "unknown_format.csv",
        )
        for name in required:
            assert _fixture(name).is_file(), f"fixture manquante: {name}"
