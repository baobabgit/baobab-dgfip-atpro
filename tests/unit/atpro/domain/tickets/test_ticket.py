"""Tests du modele Ticket."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from atpro.domain.exceptions import DomainError
from atpro.domain.tickets import Ticket


class TestTicket:
    """Instanciation Ticket."""

    def test_FEAT_005_1_instantiate_ticket(self) -> None:
        now = datetime(2026, 1, 1, tzinfo=UTC)
        ticket = Ticket(
            id="t1",
            source_system="atpro",
            external_ticket_id="TK-1",
            form_id="F1",
            form_type="demande",
            created_at=now,
            taken_at=None,
            resolved_at=None,
            closed_at=None,
            channel="phone",
            nature=None,
            ticket_type=None,
            status="open",
            contact_type=None,
            contact_identifier_hash="hash",
            creation_domain=None,
            distribution_site_id="s1",
            resolution_group_level=None,
            business_domain=None,
            owner_agent_id=None,
            qualification_agent_id=None,
            qualification_site_id=None,
            resolution_agent_id=None,
            resolution_site_id=None,
            closure_agent_id=None,
            source_import_batch_id="b1",
            line_fingerprint="fp",
            created_at_db=now,
            updated_at_db=now,
        )
        assert ticket.external_ticket_id == "TK-1"

    def test_FEAT_005_1_ticket_requires_id(self) -> None:
        now = datetime(2026, 1, 1, tzinfo=UTC)
        kwargs = {
            "form_id": None,
            "form_type": None,
            "created_at": now,
            "taken_at": None,
            "resolved_at": None,
            "closed_at": None,
            "channel": None,
            "nature": None,
            "ticket_type": None,
            "status": None,
            "contact_type": None,
            "contact_identifier_hash": None,
            "creation_domain": None,
            "distribution_site_id": None,
            "resolution_group_level": None,
            "business_domain": None,
            "owner_agent_id": None,
            "qualification_agent_id": None,
            "qualification_site_id": None,
            "resolution_agent_id": None,
            "resolution_site_id": None,
            "closure_agent_id": None,
            "source_import_batch_id": None,
            "line_fingerprint": None,
            "created_at_db": now,
            "updated_at_db": now,
        }
        with pytest.raises(DomainError):
            Ticket(id="", source_system="atpro", external_ticket_id="TK-1", **kwargs)
        with pytest.raises(DomainError):
            Ticket(id="t1", source_system=" ", external_ticket_id="TK-1", **kwargs)
        with pytest.raises(DomainError):
            Ticket(id="t1", source_system="atpro", external_ticket_id=" ", **kwargs)
