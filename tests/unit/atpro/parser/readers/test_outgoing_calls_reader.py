"""Tests de OutgoingCallsReader."""

from __future__ import annotations

from pathlib import Path

from atpro.domain.enums.call_direction import CallDirection
from atpro.parser.readers.outgoing_calls_reader import OutgoingCallsReader

_MIN_HEADER = (
    "ID de l'appel;Numero appele;Nom de l'agent;Debut d'appel;"
    "Fin d'appel;Noms de mesures;Valeurs de mesures"
)


def _write_min_csv(path: Path, body_lines: list[str]) -> None:
    path.write_text(_MIN_HEADER + "\n" + "\n".join(body_lines) + "\n", encoding="utf-8")


class TestOutgoingCallsReader:
    def test_FEAT_006_1_valid_file_two_measures(self, tmp_path: Path) -> None:
        path = tmp_path / "appels_sortants.csv"
        _write_min_csv(
            path,
            [
                "O1;0142000000;Alice DUPONT;"
                "15/06/2026 10:00:00;15/06/2026 10:05:00;"
                "Duree de communication;90",
                "O1;0142000000;Alice DUPONT;"
                "15/06/2026 10:00:00;15/06/2026 10:05:00;"
                "Duree de mise en garde;15",
            ],
        )
        result = OutgoingCallsReader().read(path)
        assert not result.errors
        assert len(result.calls) == 1
        assert result.calls[0].direction is CallDirection.OUTGOING
        assert result.calls[0].caller_hash is None
        assert result.calls[0].flow is None
        assert result.calls[0].service is None
        assert result.segments[0].talk_duration_seconds.seconds == 90
        assert result.segments[0].hold_duration_seconds.seconds == 15

    def test_FEAT_006_1_empty_caller_accepted(self, tmp_path: Path) -> None:
        path = tmp_path / "contre_appels.csv"
        path.write_text(
            "ID de l'appel;Numero appelant;Numero appele;Nom de l'agent;"
            "Debut d'appel;Fin d'appel;Noms de mesures;Valeurs de mesures\n"
            "O2;;0142000000;Bob MARTIN;"
            "15/06/2026 11:00:00;15/06/2026 11:01:00;"
            "Duree de communication;20\n",
            encoding="utf-8",
        )
        result = OutgoingCallsReader().read(path)
        assert not result.errors
        assert result.calls[0].direction is CallDirection.OUTGOING
        assert result.calls[0].caller_hash is None

    def test_FEAT_006_1_typo_filename_detected(self, tmp_path: Path) -> None:
        path = tmp_path / "appels_sotants.csv"
        _write_min_csv(
            path,
            [
                "O3;0142000000;Alice DUPONT;"
                "15/06/2026 12:00:00;15/06/2026 12:01:00;"
                "Duree de communication;10",
            ],
        )
        result = OutgoingCallsReader().read(path)
        assert not result.errors
        assert result.calls[0].direction is CallDirection.OUTGOING

    def test_FEAT_006_1_optional_columns_absent(self, tmp_path: Path) -> None:
        path = tmp_path / "sortants_min.csv"
        _write_min_csv(
            path,
            [
                "O4;0142000000;Alice DUPONT;"
                "15/06/2026 13:00:00;15/06/2026 13:02:00;"
                "Duree de communication;40",
            ],
        )
        result = OutgoingCallsReader().read(path)
        assert not result.errors
        assert result.calls[0].flow is None
        assert result.calls[0].service is None
        assert result.calls[0].caller_hash is None

    def test_FEAT_006_1_incoming_schema_warns(self, tmp_path: Path) -> None:
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
        result = OutgoingCallsReader().read(path)
        assert any(w.issue.code == "SCHEMA_NOT_OUTGOING" for w in result.warnings)

    def test_FEAT_006_1_unknown_columns_error(self, tmp_path: Path) -> None:
        path = tmp_path / "inconnu.csv"
        path.write_text("ColA;ColB\nx;y\n", encoding="utf-8")
        result = OutgoingCallsReader().read(path)
        assert any(e.issue.code == "SCHEMA_OUTGOING_REQUIRED" for e in result.errors)

    def test_FEAT_006_1_read_rows_helper(self) -> None:
        rows = [
            {
                "ID de l'appel": "O5",
                "Numero appele": "0142000000",
                "Nom de l'agent": "Alice DUPONT",
                "Debut d'appel": "15/06/2026 10:00:00",
                "Fin d'appel": "15/06/2026 10:01:00",
                "Noms de mesures": "Duree de communication",
                "Valeurs de mesures": "12",
            }
        ]
        result = OutgoingCallsReader().read_rows(rows)
        assert len(result.calls) == 1
        assert result.calls[0].direction is CallDirection.OUTGOING

    def test_FEAT_006_1_read_rows_non_outgoing_schema(self) -> None:
        rows = [
            {
                "Numero Ticket": "T1",
                "Date-Heure Creation Ticket": "15/06/2026 10:00:00",
                "Statut Ticket": "Ouvert",
                "Site Repartition Ticket": "Site A",
            }
        ]
        result = OutgoingCallsReader().read_rows(rows)
        assert any(w.issue.code == "SCHEMA_NOT_OUTGOING" for w in result.warnings)
