"""Tests du detecteur de schemas."""

from __future__ import annotations

from atpro.domain.enums import ImportFileType
from atpro.parser.detection.header_normalizer import HeaderNormalizer
from atpro.parser.schemas.schema_detector import SchemaDetector
from atpro.parser.schemas.schema_registry import SchemaRegistry


def _norm(*headers: str) -> tuple[str, ...]:
    return HeaderNormalizer().normalize_many(headers)


class TestSchemaDetector:
    def test_FEAT_002_3_incoming_calls(self) -> None:
        columns = _norm(
            "ID de l'appel",
            "Numero appelant",
            "Numero appele",
            "Nom de l'agent",
            "Debut d'appel",
            "Fin d'appel",
            "Flux",
            "Service",
            "Noms de mesures",
            "Valeurs de mesures",
        )
        match = SchemaDetector().detect(columns, already_normalized=True)
        assert match.schema_id == "incoming_calls_v1"
        assert match.file_type is ImportFileType.INCOMING_CALLS

    def test_FEAT_002_3_outgoing_calls(self) -> None:
        columns = _norm(
            "ID de l'appel",
            "Numero appele",
            "Nom de l'agent",
            "Debut d'appel",
            "Fin d'appel",
            "Noms de mesures",
            "Valeurs de mesures",
        )
        match = SchemaDetector().detect(columns, already_normalized=True)
        assert match.schema_id == "outgoing_calls_v1"
        assert match.file_type is ImportFileType.OUTGOING_CALLS

    def test_FEAT_002_3_tickets_long(self) -> None:
        columns = _norm(
            "Numero Ticket",
            "Date-Heure Creation Ticket",
            "Statut Ticket",
            "Site Repartition Ticket",
            "Canal",
            "Priorite",
            "Agent Qualification",
            "Agent Resolution",
            "Agent Cloture",
            "Groupe",
            "Domaine",
        )
        match = SchemaDetector().detect(columns, already_normalized=True)
        assert match.schema_id == "tickets_long"
        assert match.file_type is ImportFileType.TICKETS

    def test_FEAT_002_3_tickets_reduced(self) -> None:
        columns = _norm(
            "Numero Ticket",
            "Date-Heure Creation Ticket",
            "Statut Ticket",
            "Site Repartition Ticket",
        )
        match = SchemaDetector().detect(columns, already_normalized=True)
        assert match.schema_id == "tickets_reduced"

    def test_FEAT_002_3_activities_wide(self) -> None:
        columns = _norm(
            "Periode",
            "Agent / Groupe Agent",
            "Appels decroches",
            "Appels recus",
            "Temps login",
            "Temps pret",
        )
        match = SchemaDetector().detect(columns, already_normalized=True)
        assert match.schema_id == "activities_wide"
        assert match.file_type is ImportFileType.AGENT_ACTIVITIES

    def test_FEAT_002_3_activities_long(self) -> None:
        columns = _norm(
            "Periode",
            "Agent / Groupe Agent",
            "Noms de mesures",
            "Valeurs de mesures",
        )
        match = SchemaDetector().detect(columns, already_normalized=True)
        assert match.schema_id == "activities_long"

    def test_FEAT_002_3_unknown_file(self) -> None:
        match = SchemaDetector().detect(
            _norm("Colonne A", "Colonne B"),
            already_normalized=True,
        )
        assert match.schema_id == "unknown"
        assert match.file_type is ImportFileType.UNKNOWN

    def test_FEAT_002_3_extra_columns_allowed(self) -> None:
        columns = _norm(
            "Numero Ticket",
            "Date-Heure Creation Ticket",
            "Statut Ticket",
            "Site Repartition Ticket",
            "Colonne Bonus",
        )
        match = SchemaDetector().detect(columns, already_normalized=True)
        assert match.schema_id == "tickets_reduced"
        assert "colonne_bonus" in match.extra_columns
        assert any(w.issue.code == "SCHEMA_EXTRA_COLUMNS" for w in match.warnings)

    def test_FEAT_002_3_missing_required_columns(self) -> None:
        columns = _norm(
            "Numero Ticket",
            "Statut Ticket",
        )
        match = SchemaDetector().detect(columns, already_normalized=True)
        assert match.schema_id == "unknown"
        assert any(w.issue.code == "SCHEMA_MISSING_COLUMNS" for w in match.warnings)

    def test_FEAT_002_3_misleading_filename_ignored(self) -> None:
        # Nom trompeur "appels sotants" mais colonnes d'appels entrants.
        columns = _norm(
            "ID de l'appel",
            "Numero appelant",
            "Numero appele",
            "Nom de l'agent",
            "Debut d'appel",
            "Fin d'appel",
            "Flux",
            "Service",
            "Noms de mesures",
            "Valeurs de mesures",
        )
        match = SchemaDetector().detect(
            columns,
            file_name="appels_sotants.csv",
            already_normalized=True,
        )
        assert match.file_type is ImportFileType.INCOMING_CALLS
        assert match.schema_id == "incoming_calls_v1"

    def test_FEAT_002_3_raw_headers_normalized(self) -> None:
        match = SchemaDetector().detect(
            (
                "Periode",
                "Agent / Groupe Agent",
                "Noms de mesures",
                "Valeurs de mesures",
            )
        )
        assert match.schema_id == "activities_long"

    def test_FEAT_002_3_empty_registry_unknown(self) -> None:
        detector = SchemaDetector(registry=SchemaRegistry(schemas=()))
        match = detector.detect(("a",), already_normalized=True)
        assert match.schema_id == "unknown"
