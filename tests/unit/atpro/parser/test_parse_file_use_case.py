"""Tests de ParseFileUseCase."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

from atpro.domain.enums.import_file_type import ImportFileType
from atpro.domain.enums.import_severity import ImportSeverity
from atpro.domain.enums.parse_status import ParseStatus
from atpro.domain.enums.schema_version import SchemaVersion
from atpro.domain.value_objects.file_sha256 import FileSha256
from atpro.parser.activities.activity_import_result import ActivityImportResult
from atpro.parser.calls.call_consolidation_result import CallConsolidationResult
from atpro.parser.detection.file_detection_error import FileDetectionError
from atpro.parser.detection.file_inspection import FileInspection
from atpro.parser.parse_file_use_case import ParseFileUseCase
from atpro.parser.readers.incoming_calls_reader import IncomingCallsReader
from atpro.parser.readers.tickets_reader import TicketsReader
from atpro.parser.results.import_warning import ImportWarning
from atpro.parser.schemas.schema_match import SchemaMatch
from atpro.parser.tickets.ticket_import_result import TicketImportResult

_INCOMING_HEADER = (
    "ID de l'appel;Numero appelant;Numero appele;Nom de l'agent;"
    "Debut d'appel;Fin d'appel;Flux;Service;Noms de mesures;Valeurs de mesures"
)

_TICKETS_HEADER = (
    "Numero Ticket;Date-Heure Creation Ticket;Statut Ticket;"
    "Site Repartition Ticket;Canal;Nature"
)

_OUTGOING_HEADER = (
    "ID de l'appel;Numero appele;Nom de l'agent;Debut d'appel;Fin d'appel;"
    "Noms de mesures;Valeurs de mesures"
)

_ACTIVITIES_WIDE_HEADER = (
    "Periode;Agent Groupe Agent;Appels decroches;Appels recus;"
    "Temps login;Temps pret;Taux de decroches;Temps telephone"
)

_ACTIVITIES_LONG_HEADER = (
    "Periode;Agent Groupe Agent;Noms de mesures;Valeurs de mesures"
)


def _inspection(
    *,
    detected_type: ImportFileType = ImportFileType.UNKNOWN,
    schema_version: SchemaVersion = SchemaVersion.UNKNOWN,
    warnings: tuple[ImportWarning, ...] = (),
) -> FileInspection:
    return FileInspection(
        path="sample.csv",
        file_name="sample.csv",
        size_bytes=10,
        sha256=FileSha256.from_hex("a" * 64),
        encoding="utf-8",
        encoding_confidence=1.0,
        separator=";",
        separator_confidence=1.0,
        raw_columns=("col_a",),
        normalized_columns=("col_a",),
        lines_read=2,
        detected_type=detected_type,
        schema_version=schema_version,
        warnings=warnings,
    )


def _match(
    *,
    schema_id: str,
    file_type: ImportFileType,
    missing_required: tuple[str, ...] = (),
    warnings: tuple[ImportWarning, ...] = (),
) -> SchemaMatch:
    return SchemaMatch(
        schema_id=schema_id,
        file_type=file_type,
        schema_version=SchemaVersion.V1,
        score=10.0,
        confidence=1.0,
        matched_required=(),
        missing_required=missing_required,
        extra_columns=(),
        warnings=warnings,
    )


class TestParseFileUseCase:
    def test_FEAT_002_4_select_incoming_calls_reader(self, tmp_path: Path) -> None:
        path = tmp_path / "appels_entrants.csv"
        path.write_text(
            _INCOMING_HEADER + "\n" + "A1;0611111111;0142000000;Alice DUPONT;"
            "15/06/2026 10:00:00;15/06/2026 10:05:00;F1;S1;"
            "Duree de communication;120\n",
            encoding="utf-8",
        )
        incoming = MagicMock(spec=IncomingCallsReader)
        incoming.read.return_value = CallConsolidationResult(
            calls=("call",),  # type: ignore[arg-type]
            segments=("segment",),  # type: ignore[arg-type]
        )
        outgoing = MagicMock()
        tickets = MagicMock()
        use_case = ParseFileUseCase(
            incoming_calls_reader=incoming,
            outgoing_calls_reader=outgoing,
            tickets_reader=tickets,
        )
        result = use_case.parse(path)
        incoming.read.assert_called_once_with(path)
        outgoing.read.assert_not_called()
        tickets.read.assert_not_called()
        assert result.records == ("call", "segment")
        assert result.detected_type is ImportFileType.INCOMING_CALLS

    def test_FEAT_002_4_select_tickets_reader(self, tmp_path: Path) -> None:
        path = tmp_path / "tickets.csv"
        path.write_text(
            _TICKETS_HEADER
            + "\n"
            + "T1;15/06/2026 10:00:00;Ouvert;Site A;Chat;Incident\n",
            encoding="utf-8",
        )
        tickets = MagicMock(spec=TicketsReader)
        tickets.read.return_value = TicketImportResult(tickets=("ticket",))  # type: ignore[arg-type]
        incoming = MagicMock()
        use_case = ParseFileUseCase(
            incoming_calls_reader=incoming,
            tickets_reader=tickets,
        )
        result = use_case.parse(path)
        tickets.read.assert_called_once_with(path)
        incoming.read.assert_not_called()
        assert result.records == ("ticket",)
        assert result.detected_type is ImportFileType.TICKETS

    def test_FEAT_002_4_unknown_type(self, tmp_path: Path) -> None:
        path = tmp_path / "inconnu.csv"
        path.write_text("foo;bar\n1;2\n", encoding="utf-8")
        result = ParseFileUseCase().parse(path)
        assert result.detected_type is ImportFileType.UNKNOWN
        assert result.records == ()
        assert any(e.issue.code == "FILE_TYPE_UNKNOWN" for e in result.errors)
        assert result.summary.status is ParseStatus.FAILED

    def test_FEAT_002_4_reader_error_converted(self, tmp_path: Path) -> None:
        path = tmp_path / "absent.csv"
        result = ParseFileUseCase().parse(path)
        assert result.records == ()
        assert len(result.errors) == 1
        assert result.errors[0].issue.code == "FILE_ABSENT"
        assert result.errors[0].issue.severity is ImportSeverity.FATAL
        assert result.summary.status is ParseStatus.FAILED
        assert result.file_metadata.detected_type is ImportFileType.UNKNOWN

    def test_FEAT_002_4_valid_result(self, tmp_path: Path) -> None:
        path = tmp_path / "appels_entrants.csv"
        path.write_text(
            _INCOMING_HEADER + "\n" + "A1;0611111111;0142000000;Alice DUPONT;"
            "15/06/2026 10:00:00;15/06/2026 10:05:00;F1;S1;"
            "Duree de communication;120\n" + "A1;0611111111;0142000000;Alice DUPONT;"
            "15/06/2026 10:00:00;15/06/2026 10:05:00;F1;S1;"
            "Duree de mise en garde;30\n",
            encoding="utf-8",
        )
        result = ParseFileUseCase().parse(path)
        assert not result.errors
        assert result.summary.status is ParseStatus.SUCCESS
        assert result.summary.record_count >= 2
        assert result.detected_type is ImportFileType.INCOMING_CALLS

    def test_FEAT_002_4_invalid_result(self, tmp_path: Path) -> None:
        path = tmp_path / "tickets_bad.csv"
        path.write_text(
            _TICKETS_HEADER
            + ";Date-Heure Resolution Ticket\n"
            + "T103;15/06/2026 10:00:00;Clos;Site A;Tel;Demande;"
            "14/06/2026 10:00:00\n",
            encoding="utf-8",
        )
        result = ParseFileUseCase().parse(path)
        assert any(
            e.issue.code == "TICKET_RESOLVED_BEFORE_CREATED" for e in result.errors
        )
        assert result.records == ()

    def test_FEAT_002_4_preview_limited(self, tmp_path: Path) -> None:
        path = tmp_path / "tickets_many.csv"
        lines = [
            _TICKETS_HEADER,
            "T1;15/06/2026 10:00:00;Ouvert;Site A;Chat;Incident",
            "T2;15/06/2026 11:00:00;Ouvert;Site B;Mail;Demande",
            "T3;15/06/2026 12:00:00;Ouvert;Site C;Tel;Question",
        ]
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        preview = ParseFileUseCase().preview(path, limit=2)
        assert preview.limit == 2
        assert len(preview.records) == 2
        assert not preview.errors

    def test_FEAT_002_4_validate_matches_parse_status(self, tmp_path: Path) -> None:
        path = tmp_path / "appels_entrants.csv"
        path.write_text(
            _INCOMING_HEADER + "\n" + "A1;0611111111;0142000000;Alice DUPONT;"
            "15/06/2026 10:00:00;15/06/2026 10:05:00;F1;S1;"
            "Duree de communication;120\n",
            encoding="utf-8",
        )
        use_case = ParseFileUseCase()
        parsed = use_case.parse(path)
        validated = use_case.validate(path)
        assert validated.summary.status is parsed.summary.status
        assert validated.detected_type is parsed.detected_type

    def test_FEAT_002_4_inspect_enriches_type(self, tmp_path: Path) -> None:
        path = tmp_path / "appels_entrants.csv"
        path.write_text(
            _INCOMING_HEADER + "\n" + "A1;0611111111;0142000000;Alice DUPONT;"
            "15/06/2026 10:00:00;15/06/2026 10:05:00;F1;S1;"
            "Duree de communication;120\n",
            encoding="utf-8",
        )
        inspection = ParseFileUseCase().inspect(path)
        assert inspection.detected_type is ImportFileType.INCOMING_CALLS
        assert inspection.schema_version is SchemaVersion.V1

    def test_FEAT_002_4_select_outgoing_calls_reader(self, tmp_path: Path) -> None:
        path = tmp_path / "appels_sortants.csv"
        path.write_text(
            _OUTGOING_HEADER + "\n" + "O1;0142000000;Bob MARTIN;"
            "15/06/2026 10:00:00;15/06/2026 10:01:00;"
            "Duree de communication;10\n",
            encoding="utf-8",
        )
        result = ParseFileUseCase().parse(path)
        assert result.detected_type is ImportFileType.OUTGOING_CALLS
        assert result.summary.record_count >= 1

    def test_FEAT_002_4_select_activities_wide_reader(self, tmp_path: Path) -> None:
        path = tmp_path / "activities_wide.csv"
        path.write_text(
            _ACTIVITIES_WIDE_HEADER
            + "\n"
            + "15/06/2026;Alice DUPONT;8;10;01:00:00;00:45:00;80,00%;00:30:00\n",
            encoding="utf-8",
        )
        result = ParseFileUseCase().parse(path)
        assert result.detected_type is ImportFileType.AGENT_ACTIVITIES
        assert not result.errors
        assert result.summary.record_count == 1

    def test_FEAT_002_4_select_activities_long_reader(self, tmp_path: Path) -> None:
        path = tmp_path / "activities_long.csv"
        path.write_text(
            _ACTIVITIES_LONG_HEADER
            + "\n"
            + "15/06/2026;Alice DUPONT;Appels decroches;5\n"
            + "15/06/2026;Alice DUPONT;Appels recus;8\n",
            encoding="utf-8",
        )
        result = ParseFileUseCase().parse(path)
        assert result.detected_type is ImportFileType.AGENT_ACTIVITIES
        assert not result.errors
        assert result.summary.record_count == 1

    def test_FEAT_002_4_activities_unsupported_schema(self) -> None:
        inspector = MagicMock()
        base = _inspection()
        inspector.inspect.return_value = base
        detector = MagicMock()
        detector.detect.return_value = _match(
            schema_id="activities_weird",
            file_type=ImportFileType.AGENT_ACTIVITIES,
        )
        use_case = ParseFileUseCase(
            inspector=inspector,
            schema_detector=detector,
        )
        result = use_case.parse(Path("x.csv"))
        assert any(
            e.issue.code == "SCHEMA_ACTIVITIES_UNSUPPORTED" for e in result.errors
        )
        assert result.records == ()

    def test_FEAT_002_4_schema_missing_columns_error(self) -> None:
        inspector = MagicMock()
        inspector.inspect.return_value = _inspection()
        detector = MagicMock()
        detector.detect.return_value = _match(
            schema_id="incoming_calls_v1",
            file_type=ImportFileType.INCOMING_CALLS,
            missing_required=("flux", "service"),
        )
        incoming = MagicMock()
        incoming.read.return_value = CallConsolidationResult(calls=(), segments=())
        use_case = ParseFileUseCase(
            inspector=inspector,
            schema_detector=detector,
            incoming_calls_reader=incoming,
        )
        result = use_case.parse(Path("x.csv"))
        assert any(e.issue.code == "SCHEMA_MISSING_COLUMNS" for e in result.errors)
        incoming.read.assert_called_once()

    def test_FEAT_002_4_public_import(self) -> None:
        from atpro.parser import ParseFileUseCase as Exported

        assert Exported is ParseFileUseCase

    def test_FEAT_002_4_empty_file_converted(self, tmp_path: Path) -> None:
        path = tmp_path / "empty.csv"
        path.write_text("", encoding="utf-8")
        result = ParseFileUseCase().parse(path)
        assert result.errors[0].issue.code == "FILE_EMPTY"
        assert result.errors[0].issue.severity is ImportSeverity.FATAL

    def test_FEAT_002_4_inspect_merges_schema_warnings(self) -> None:
        inspector = MagicMock()
        base = _inspection(
            warnings=(ImportWarning.create(code="ENC_DEGRADED", message="enc"),)
        )
        inspector.inspect.return_value = base
        detector = MagicMock()
        detector.detect.return_value = _match(
            schema_id="incoming_calls_v1",
            file_type=ImportFileType.INCOMING_CALLS,
            warnings=(
                ImportWarning.create(code="SCHEMA_EXTRA_COLUMNS", message="extra"),
            ),
        )
        inspection = ParseFileUseCase(
            inspector=inspector,
            schema_detector=detector,
        ).inspect(Path("x.csv"))
        codes = {w.issue.code for w in inspection.warnings}
        assert "ENC_DEGRADED" in codes
        assert "SCHEMA_EXTRA_COLUMNS" in codes
        assert inspection.detected_type is ImportFileType.INCOMING_CALLS

    def test_FEAT_002_4_detection_error_from_reader_path(self) -> None:
        """FileDetectionError levee hors inspect enrichi reste convertie via parse.

        Cas couvert : inspect reussi puis reader qui leve (non attendu en prod) ;
        ici on simule l'echec des le inspect.
        """
        inspector = MagicMock()
        inspector.inspect.side_effect = FileDetectionError(
            "FILE_ABSENT", "fichier absent: x.csv"
        )
        result = ParseFileUseCase(inspector=inspector).parse(Path("x.csv"))
        assert result.file_metadata.encoding == "?"
        assert result.file_metadata.separator == ";"
        assert result.errors[0].issue.code == "FILE_ABSENT"

    def test_FEAT_002_4_activities_wide_via_mock(self) -> None:
        inspector = MagicMock()
        inspector.inspect.return_value = _inspection()
        detector = MagicMock()
        detector.detect.return_value = _match(
            schema_id="activities_wide",
            file_type=ImportFileType.AGENT_ACTIVITIES,
        )
        wide = MagicMock()
        wide.read.return_value = ActivityImportResult(activities=("act",))  # type: ignore[arg-type]
        long = MagicMock()
        use_case = ParseFileUseCase(
            inspector=inspector,
            schema_detector=detector,
            activities_wide_reader=wide,
            activities_long_reader=long,
        )
        result = use_case.parse(Path("x.csv"))
        wide.read.assert_called_once()
        long.read.assert_not_called()
        assert result.records == ("act",)

    def test_FEAT_002_4_activities_long_via_mock(self) -> None:
        inspector = MagicMock()
        inspector.inspect.return_value = _inspection()
        detector = MagicMock()
        detector.detect.return_value = _match(
            schema_id="activities_long",
            file_type=ImportFileType.AGENT_ACTIVITIES,
        )
        wide = MagicMock()
        long = MagicMock()
        long.read.return_value = ActivityImportResult(activities=("act",))  # type: ignore[arg-type]
        use_case = ParseFileUseCase(
            inspector=inspector,
            schema_detector=detector,
            activities_wide_reader=wide,
            activities_long_reader=long,
        )
        result = use_case.parse(Path("x.csv"))
        long.read.assert_called_once()
        wide.read.assert_not_called()
        assert result.records == ("act",)

    def test_FEAT_002_4_run_reader_unknown_fallback(self) -> None:
        use_case = ParseFileUseCase()
        records, errors, _warnings = use_case._run_reader(
            Path("x.csv"),
            file_type=ImportFileType.UNKNOWN,
            schema_id="unknown",
            inspection=_inspection(),
        )
        assert records == ()
        assert errors[0].issue.code == "FILE_TYPE_UNKNOWN"
