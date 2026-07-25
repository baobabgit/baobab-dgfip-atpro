"""Tests de TicketBuilder."""

from __future__ import annotations

from atpro.parser.tickets.raw_ticket_row import RawTicketRow
from atpro.parser.tickets.ticket_builder import TicketBuilder


def _row(**overrides: object) -> RawTicketRow:
    base: dict[str, object] = {
        "row_number": 2,
        "external_ticket_id": "T1",
        "created_at_raw": "15/06/2026 10:00:00",
        "taken_at_raw": None,
        "resolved_at_raw": None,
        "closed_at_raw": None,
        "channel": "Telephone",
        "nature": "Demande",
        "ticket_type": "Standard",
        "status": "Ouvert",
        "distribution_site": "Site A",
        "qualification_agent": "Alice DUPONT",
        "qualification_site": None,
        "resolution_agent": None,
        "resolution_site": None,
        "closure_agent": None,
        "group": None,
        "domain": None,
        "contact_type": None,
        "contact_identifier": "user@example.com",
        "form_id": None,
        "form_type": None,
    }
    base.update(overrides)
    return RawTicketRow(**base)  # type: ignore[arg-type]


class TestTicketBuilder:
    def test_FEAT_007_1_hashes_email_contact(self) -> None:
        result = TicketBuilder().build([_row()])
        assert len(result.tickets) == 1
        assert result.tickets[0].contact_identifier_hash is not None
        assert "example.com" not in (result.tickets[0].contact_identifier_hash or "")

    def test_FEAT_007_1_closed_before_created(self) -> None:
        result = TicketBuilder().build(
            [
                _row(
                    closed_at_raw="14/06/2026 09:00:00",
                    status="Clos",
                )
            ]
        )
        assert any(
            e.issue.code == "TICKET_CLOSED_BEFORE_CREATED" for e in result.errors
        )
        assert result.tickets == ()

    def test_FEAT_007_1_invalid_dates(self) -> None:
        result = TicketBuilder().build(
            [
                _row(
                    created_at_raw="pas-une-date",
                    taken_at_raw="toujours-non",
                )
            ]
        )
        assert any(e.issue.code == "TICKET_DATE_INVALID" for e in result.errors)
        assert result.tickets == ()

    def test_FEAT_007_1_missing_created_at(self) -> None:
        result = TicketBuilder().build([_row(created_at_raw=None)])
        assert any(e.issue.code == "TICKET_CREATED_AT_REQUIRED" for e in result.errors)

    def test_FEAT_007_1_empty_site_and_agent_warn(self) -> None:
        result = TicketBuilder().build(
            [_row(distribution_site="   ", qualification_agent="   ")]
        )
        assert any(w.issue.code == "TICKET_SITE_MISSING" for w in result.warnings)
        assert any(w.issue.code == "TICKET_AGENT_MISSING" for w in result.warnings)
        assert len(result.tickets) == 1

    def test_FEAT_007_1_blank_contact_hash_none(self) -> None:
        result = TicketBuilder().build([_row(contact_identifier="")])
        assert result.tickets[0].contact_identifier_hash is None
