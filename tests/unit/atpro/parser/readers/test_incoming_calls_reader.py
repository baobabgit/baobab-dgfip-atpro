"""Tests de IncomingCallsReader."""

from __future__ import annotations

from pathlib import Path

from atpro.domain.enums.call_direction import CallDirection
from atpro.parser.readers.incoming_calls_reader import IncomingCallsReader

_HEADER = (
    "ID de l'appel;Numero appelant;Numero appele;Nom de l'agent;"
    "Debut d'appel;Fin d'appel;Flux;Service;Noms de mesures;Valeurs de mesures"
)


def _write_csv(path: Path, body_lines: list[str]) -> None:
    path.write_text(_HEADER + "\n" + "\n".join(body_lines) + "\n", encoding="utf-8")


_FIXTURE_INCOMING = (
    Path(__file__).resolve().parents[4]
    / "fixtures"
    / "csv"
    / "incoming_calls_valid.csv"
)


class TestIncomingCallsReader:
    def test_FEAT_005_4_valid_file_two_measures(self) -> None:
        result = IncomingCallsReader().read(_FIXTURE_INCOMING)
        assert not result.errors
        assert len(result.calls) >= 1
        alice = next(c for c in result.calls if c.external_call_id == "A100")
        assert alice.direction is CallDirection.INCOMING
        assert alice.flow == "Flux Standard"
        assert alice.service == "Service Accueil"
        alice_seg = next(s for s in result.segments if s.call_id == alice.id)
        assert alice_seg.talk_duration_seconds.seconds == 120
        assert alice_seg.hold_duration_seconds.seconds == 30
        assert alice_seg.raw_agent_name == "Alice DUPONT"

    def test_FEAT_005_4_historical_date_format(self, tmp_path: Path) -> None:
        path = tmp_path / "historique.csv"
        _write_csv(
            path,
            [
                "A2;0611111111;0142000000;Bob MARTIN;"
                "15-06-26 09:00:00;15-06-26 09:01:00;F1;S1;"
                "Duree de communication;0",
            ],
        )
        result = IncomingCallsReader().read(path)
        assert not result.errors
        assert result.segments[0].talk_duration_seconds.seconds == 0
        assert result.calls[0].started_at.year == 2026

    def test_FEAT_005_4_multi_line_call(self, tmp_path: Path) -> None:
        path = tmp_path / "multi_lignes.csv"
        _write_csv(
            path,
            [
                "A3;0611111111;0142000000;Alice DUPONT;"
                "15/06/2026 10:00:00;15/06/2026 10:05:00;F1;S1;"
                "Duree de communication;100",
                "A3;0611111111;0142000000;Alice DUPONT;"
                "15/06/2026 10:00:00;15/06/2026 10:05:00;F1;S1;"
                "Duree de mise en garde;20",
            ],
        )
        result = IncomingCallsReader().read(path)
        assert result.segments[0].source_row_numbers == (2, 3)

    def test_FEAT_005_4_multi_segments(self, tmp_path: Path) -> None:
        path = tmp_path / "multi_segments.csv"
        _write_csv(
            path,
            [
                "A4;0611111111;0142000000;Alice DUPONT;"
                "15/06/2026 10:00:00;15/06/2026 10:02:00;F1;S1;"
                "Duree de communication;60",
                "A4;0611111111;0142000000;Bob MARTIN;"
                "15/06/2026 10:02:00;15/06/2026 10:05:00;F1;S1;"
                "Duree de communication;40",
            ],
        )
        result = IncomingCallsReader().read(path)
        assert len(result.calls) == 1
        assert len(result.segments) == 2
        assert any(w.issue.code == "CALL_MULTI_SEGMENT" for w in result.warnings)

    def test_FEAT_005_4_unknown_measure(self, tmp_path: Path) -> None:
        path = tmp_path / "unknown_measure.csv"
        _write_csv(
            path,
            [
                "A5;0611111111;0142000000;Alice DUPONT;"
                "15/06/2026 10:00:00;15/06/2026 10:01:00;F1;S1;"
                "Duree de communication;10",
                "A5;0611111111;0142000000;Alice DUPONT;"
                "15/06/2026 10:00:00;15/06/2026 10:01:00;F1;S1;"
                "Mesure inconnue;1",
            ],
        )
        result = IncomingCallsReader().read(path)
        assert any(w.issue.code == "CALL_MEASURE_UNKNOWN" for w in result.warnings)

    def test_FEAT_005_4_read_rows_helper(self) -> None:
        rows = [
            {
                "ID de l'appel": "A6",
                "Numero appelant": "0611111111",
                "Numero appele": "0142000000",
                "Nom de l'agent": "Alice DUPONT",
                "Debut d'appel": "15/06/2026 10:00:00",
                "Fin d'appel": "15/06/2026 10:01:00",
                "Flux": "F1",
                "Service": "S1",
                "Noms de mesures": "Duree de communication",
                "Valeurs de mesures": "15",
            }
        ]
        result = IncomingCallsReader().read_rows(rows)
        assert len(result.calls) == 1
        assert result.calls[0].direction is CallDirection.INCOMING

    def test_FEAT_005_4_incompatible_schema_file(self, tmp_path: Path) -> None:
        path = tmp_path / "tickets.csv"
        path.write_text(
            "Numero Ticket;Date-Heure Creation Ticket;Statut Ticket;"
            "Site Repartition Ticket\n"
            "T1;15/06/2026 10:00:00;Ouvert;Site A\n",
            encoding="utf-8",
        )
        result = IncomingCallsReader().read(path)
        assert any(w.issue.code == "SCHEMA_NOT_INCOMING" for w in result.warnings)

    def test_FEAT_005_4_unknown_columns_error(self, tmp_path: Path) -> None:
        path = tmp_path / "inconnu.csv"
        path.write_text("ColA;ColB\nx;y\n", encoding="utf-8")
        result = IncomingCallsReader().read(path)
        assert any(e.issue.code == "SCHEMA_INCOMING_REQUIRED" for e in result.errors)

    def test_FEAT_005_4_outgoing_schema_warns(self, tmp_path: Path) -> None:
        path = tmp_path / "sortants.csv"
        path.write_text(
            "ID de l'appel;Numero appele;Nom de l'agent;Debut d'appel;"
            "Fin d'appel;Noms de mesures;Valeurs de mesures\n"
            "O1;0142000000;Alice DUPONT;15/06/2026 10:00:00;"
            "15/06/2026 10:01:00;Duree de communication;10\n",
            encoding="utf-8",
        )
        result = IncomingCallsReader().read(path)
        assert any(w.issue.code == "SCHEMA_NOT_INCOMING" for w in result.warnings)

    def test_FEAT_005_4_read_rows_non_incoming_schema(self) -> None:
        rows = [
            {
                "Numero Ticket": "T1",
                "Date-Heure Creation Ticket": "15/06/2026 10:00:00",
                "Statut Ticket": "Ouvert",
                "Site Repartition Ticket": "Site A",
            }
        ]
        result = IncomingCallsReader().read_rows(rows)
        assert any(w.issue.code == "SCHEMA_NOT_INCOMING" for w in result.warnings)
