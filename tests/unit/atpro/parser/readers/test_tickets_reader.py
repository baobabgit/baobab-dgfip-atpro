"""Tests de TicketsReader."""

from __future__ import annotations

from pathlib import Path

from atpro.parser.readers.tickets_reader import TicketsReader

_FIXTURE_TICKETS_LONG = (
    Path(__file__).resolve().parents[4] / "fixtures" / "csv" / "tickets_long_valid.csv"
)

_LONG_HEADER = (
    "Numero Ticket;Date-Heure Creation Ticket;Date-Heure Prise en Charge Ticket;"
    "Date-Heure Resolution Ticket;Date-Heure Cloture Ticket;Statut Ticket;"
    "Site Repartition Ticket;Canal;Priorite;Agent Qualification;Agent Resolution;"
    "Agent Cloture;Groupe;Domaine;Nature Ticket;Type Ticket;Telephone Contact"
)

_REDUCED_HEADER = (
    "Numero Ticket;Date-Heure Creation Ticket;Statut Ticket;"
    "Site Repartition Ticket;Canal;Nature"
)


class TestTicketsReader:
    def test_FEAT_007_1_closed_ticket_long_schema(self) -> None:
        result = TicketsReader().read(_FIXTURE_TICKETS_LONG)
        assert not result.errors
        assert len(result.tickets) >= 1
        ticket = next(t for t in result.tickets if t.external_ticket_id == "T100")
        assert ticket.status == "clos"
        assert ticket.channel == "telephone"
        assert ticket.resolved_at is not None
        assert ticket.closed_at is not None
        assert ticket.contact_identifier_hash is not None
        assert "0611111111" not in str(ticket)
        assert ticket.qualification_agent_id is not None
        assert ticket.distribution_site_id is not None
        assert result.agent_identities
        assert result.site_identities

    def test_FEAT_007_1_open_ticket_no_resolution(self, tmp_path: Path) -> None:
        path = tmp_path / "tickets_open.csv"
        path.write_text(
            _LONG_HEADER + "\n" + "T101;15/06/2026 09:00:00;15/06/2026 09:10:00;;;"
            "Ouvert;Site Lyon;Mail;Normale;Alice DUPONT;;;"
            "N2;RH;Question;Standard;\n",
            encoding="utf-8",
        )
        result = TicketsReader().read(path)
        assert not result.errors
        assert len(result.tickets) == 1
        assert result.tickets[0].resolved_at is None
        assert result.tickets[0].closed_at is None
        assert result.tickets[0].status == "ouvert"

    def test_FEAT_007_1_reduced_schema(self, tmp_path: Path) -> None:
        path = tmp_path / "tickets_reduced.csv"
        path.write_text(
            _REDUCED_HEADER
            + "\n"
            + "T102;16/06/2026 08:00:00;Ouvert;Site Lille;Chat;Incident\n",
            encoding="utf-8",
        )
        result = TicketsReader().read(path)
        assert not result.errors
        assert len(result.tickets) == 1
        assert result.tickets[0].external_ticket_id == "T102"
        assert result.tickets[0].nature == "incident"
        assert result.tickets[0].channel == "chat"

    def test_FEAT_007_1_incoherent_resolution_date(self, tmp_path: Path) -> None:
        path = tmp_path / "tickets_bad_date.csv"
        path.write_text(
            _REDUCED_HEADER
            + ";Date-Heure Resolution Ticket\n"
            + "T103;15/06/2026 10:00:00;Clos;Site A;Tel;Demande;"
            "14/06/2026 10:00:00\n",
            encoding="utf-8",
        )
        result = TicketsReader().read(path)
        assert any(
            e.issue.code == "TICKET_RESOLVED_BEFORE_CREATED" for e in result.errors
        )
        assert result.tickets == ()

    def test_FEAT_007_1_degraded_encoding(self, tmp_path: Path) -> None:
        path = tmp_path / "tickets_cp1252.csv"
        content = (
            "Numero Ticket;Date-Heure Creation Ticket;Statut Ticket;"
            "Site Repartition Ticket\n"
            "T104;15/06/2026 10:00:00;Ouvert;Site Créteil\n"
        )
        path.write_bytes(content.encode("cp1252"))
        result = TicketsReader().read(path)
        assert not result.errors
        assert len(result.tickets) == 1
        assert result.tickets[0].distribution_site_id is not None

    def test_FEAT_007_1_missing_ticket_id(self, tmp_path: Path) -> None:
        path = tmp_path / "tickets_no_id.csv"
        path.write_text(
            _REDUCED_HEADER + "\n" ";15/06/2026 10:00:00;Ouvert;Site A;Tel;Demande\n",
            encoding="utf-8",
        )
        result = TicketsReader().read(path)
        assert any(e.issue.code == "TICKET_ID_REQUIRED" for e in result.errors)

    def test_FEAT_007_1_read_rows_helper(self) -> None:
        rows = [
            {
                "Numero Ticket": "T105",
                "Date-Heure Creation Ticket": "15/06/2026 10:00:00",
                "Statut Ticket": "Ouvert",
                "Site Repartition Ticket": "Site A",
            }
        ]
        result = TicketsReader().read_rows(rows)
        assert len(result.tickets) == 1
        assert result.tickets[0].external_ticket_id == "T105"

    def test_FEAT_007_1_unknown_schema_error(self, tmp_path: Path) -> None:
        path = tmp_path / "inconnu.csv"
        path.write_text("ColA;ColB\nx;y\n", encoding="utf-8")
        result = TicketsReader().read(path)
        assert any(e.issue.code == "SCHEMA_TICKETS_REQUIRED" for e in result.errors)

    def test_FEAT_007_1_non_tickets_schema_warns(self) -> None:
        rows = [
            {
                "ID de l'appel": "A1",
                "Numero appelant": "0611111111",
                "Numero appele": "0142000000",
                "Nom de l'agent": "Alice DUPONT",
                "Debut d'appel": "15/06/2026 10:00:00",
                "Fin d'appel": "15/06/2026 10:01:00",
                "Flux": "F1",
                "Service": "S1",
                "Noms de mesures": "Duree de communication",
                "Valeurs de mesures": "10",
            }
        ]
        result = TicketsReader().read_rows(rows)
        assert any(w.issue.code == "SCHEMA_NOT_TICKETS" for w in result.warnings)

    def test_FEAT_007_1_incoming_file_warns(self, tmp_path: Path) -> None:
        path = tmp_path / "entrants.csv"
        path.write_text(
            "ID de l'appel;Numero appelant;Numero appele;Nom de l'agent;"
            "Debut d'appel;Fin d'appel;Flux;Service;"
            "Noms de mesures;Valeurs de mesures\n"
            "A1;0611111111;0142000000;Alice DUPONT;"
            "15/06/2026 10:00:00;15/06/2026 10:01:00;F1;S1;"
            "Duree de communication;10\n",
            encoding="utf-8",
        )
        result = TicketsReader().read(path)
        assert any(w.issue.code == "SCHEMA_NOT_TICKETS" for w in result.warnings)

    def test_FEAT_007_1_missing_site_warns(self, tmp_path: Path) -> None:
        path = tmp_path / "no_site.csv"
        path.write_text(
            "Numero Ticket;Date-Heure Creation Ticket;Statut Ticket;"
            "Site Repartition Ticket\n"
            "T200;15/06/2026 10:00:00;Ouvert;\n",
            encoding="utf-8",
        )
        result = TicketsReader().read(path)
        assert any(w.issue.code == "TICKET_SITE_MISSING" for w in result.warnings)
        assert len(result.tickets) == 1
