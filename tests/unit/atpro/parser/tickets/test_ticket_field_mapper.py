"""Tests de TicketFieldMapper."""

from __future__ import annotations

from atpro.parser.tickets.ticket_field_mapper import TicketFieldMapper


class TestTicketFieldMapper:
    def test_FEAT_007_1_maps_split_agent_names(self) -> None:
        row = TicketFieldMapper().map_row(
            2,
            {
                "Numero Ticket": "T1",
                "Date-Heure Creation Ticket": "15/06/2026 10:00:00",
                "Statut Ticket": "Ouvert",
                "Site Repartition Ticket": "Site A",
                "Prenom Agent Qualification Ticket": "Alice",
                "Nom Agent Qualification Ticket": "DUPONT",
            },
        )
        assert row.qualification_agent == "Alice DUPONT"
        assert row.external_ticket_id == "T1"
