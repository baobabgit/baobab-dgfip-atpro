"""Point d'entree public du parsing CSV.

:spec: FEAT-002.4
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any

from atpro.domain.enums.import_file_type import ImportFileType
from atpro.domain.enums.import_severity import ImportSeverity
from atpro.domain.enums.schema_version import SchemaVersion
from atpro.domain.value_objects.file_sha256 import FileSha256
from atpro.parser.detection.file_detection_error import FileDetectionError
from atpro.parser.detection.file_inspection import FileInspection
from atpro.parser.detection.file_inspector import FileInspector
from atpro.parser.readers.agent_activities_long_reader import AgentActivitiesLongReader
from atpro.parser.readers.agent_activities_wide_reader import AgentActivitiesWideReader
from atpro.parser.readers.incoming_calls_reader import IncomingCallsReader
from atpro.parser.readers.outgoing_calls_reader import OutgoingCallsReader
from atpro.parser.readers.tickets_reader import TicketsReader
from atpro.parser.results.file_metadata import FileMetadata
from atpro.parser.results.import_error import ImportError
from atpro.parser.results.import_warning import ImportWarning
from atpro.parser.results.parse_preview import ParsePreview
from atpro.parser.results.parse_result import ParseResult
from atpro.parser.schemas.schema_detector import SchemaDetector
from atpro.parser.schemas.schema_match import SchemaMatch

_EMPTY_SHA256 = FileSha256.from_hex(
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)


class ParseFileUseCase:
    """Orchestrateur unique : inspecter, valider, previsualiser et parser.

    Ne depend pas de PostgreSQL. Selectionne le reader selon le type et le
    schema detectes, puis assemble un ``ParseResult`` standardise.

    :spec: FEAT-002.4
    """

    def __init__(
        self,
        *,
        inspector: FileInspector | None = None,
        schema_detector: SchemaDetector | None = None,
        incoming_calls_reader: IncomingCallsReader | None = None,
        outgoing_calls_reader: OutgoingCallsReader | None = None,
        tickets_reader: TicketsReader | None = None,
        activities_wide_reader: AgentActivitiesWideReader | None = None,
        activities_long_reader: AgentActivitiesLongReader | None = None,
    ) -> None:
        """Injecte les collaborateurs (tests).

        :param inspector: Inspection bas niveau du fichier.
        :param schema_detector: Detection de schema.
        :param incoming_calls_reader: Reader appels entrants.
        :param outgoing_calls_reader: Reader appels sortants.
        :param tickets_reader: Reader tickets.
        :param activities_wide_reader: Reader activites format large.
        :param activities_long_reader: Reader activites format long.
        """
        self._inspector = inspector or FileInspector()
        self._schema_detector = schema_detector or SchemaDetector()
        self._incoming = incoming_calls_reader or IncomingCallsReader()
        self._outgoing = outgoing_calls_reader or OutgoingCallsReader()
        self._tickets = tickets_reader or TicketsReader()
        self._activities_wide = activities_wide_reader or AgentActivitiesWideReader()
        self._activities_long = activities_long_reader or AgentActivitiesLongReader()

    def inspect(self, path: Path) -> FileInspection:
        """Inspecte le fichier et enrichit type / schema detectes.

        :param path: Chemin du fichier CSV.
        :returns: Inspection enrichie (type, schema, warnings fusionnes).
        :raises FileDetectionError: Fichier absent ou vide.
        :spec: FEAT-002.4
        """
        inspection, _match = self._inspect_enriched(path)
        return inspection

    def validate(self, path: Path) -> ParseResult:
        """Valide un fichier (meme logique que ``parse`` en v0.1).

        :param path: Chemin du fichier CSV.
        :returns: Resultat standardise (sans exception technique non convertie).
        :spec: FEAT-002.4
        """
        return self.parse(path)

    def preview(self, path: Path, limit: int = 10) -> ParsePreview:
        """Parse puis retourne les ``limit`` premiers enregistrements.

        :param path: Chemin du fichier CSV.
        :param limit: Nombre maximum d'enregistrements a exposer.
        :returns: Apercu avec metadonnees / erreurs / warnings complets.
        :spec: FEAT-002.4
        """
        result = self.parse(path)
        return ParsePreview(
            file_metadata=result.file_metadata,
            limit=limit,
            records=result.records[:limit],
            warnings=result.warnings,
            errors=result.errors,
        )

    def parse(self, path: Path) -> ParseResult:
        """Parse un fichier CSV via le reader adequat.

        :param path: Chemin du fichier CSV.
        :returns: Resultat standardise ; erreurs techniques converties.
        :spec: FEAT-002.4
        """
        try:
            inspection, match = self._inspect_enriched(path)
        except FileDetectionError as exc:
            return self._from_detection_error(path, exc)

        metadata = self._metadata_from_inspection(inspection)
        extra_errors: list[ImportError] = []
        if match.missing_required and match.schema_id != "unknown":
            listed = ", ".join(match.missing_required)
            extra_errors.append(
                ImportError.create(
                    code="SCHEMA_MISSING_COLUMNS",
                    message=(
                        "colonnes obligatoires absentes pour le schema "
                        f"{match.schema_id}: {listed}"
                    ),
                    hint="verifier l'export source ou la variante de schema",
                )
            )

        if inspection.detected_type is ImportFileType.UNKNOWN:
            return ParseResult.build(
                file_metadata=metadata,
                warnings=inspection.warnings,
                errors=(
                    *extra_errors,
                    ImportError.create(
                        code="FILE_TYPE_UNKNOWN",
                        message="type de fichier non reconnu",
                        hint="verifier les colonnes ou le nom du fichier",
                    ),
                ),
            )

        records, reader_errors, reader_warnings = self._run_reader(
            path,
            file_type=inspection.detected_type,
            schema_id=match.schema_id,
            inspection=inspection,
        )
        return ParseResult.build(
            file_metadata=metadata,
            records=records,
            warnings=reader_warnings,
            errors=(*extra_errors, *reader_errors),
        )

    def _inspect_enriched(self, path: Path) -> tuple[FileInspection, SchemaMatch]:
        """Inspecte puis detecte le schema.

        :param path: Chemin du fichier.
        :returns: Inspection enrichie et match de schema.
        :raises FileDetectionError: Detection fatale.
        """
        base = self._inspector.inspect(path)
        match = self._schema_detector.detect(
            base.normalized_columns,
            file_name=base.file_name,
            already_normalized=True,
        )
        enriched = replace(
            base,
            detected_type=match.file_type,
            schema_version=match.schema_version,
            warnings=(*base.warnings, *match.warnings),
        )
        return enriched, match

    def _run_reader(
        self,
        path: Path,
        *,
        file_type: ImportFileType,
        schema_id: str,
        inspection: FileInspection,
    ) -> tuple[tuple[Any, ...], tuple[ImportError, ...], tuple[ImportWarning, ...]]:
        """Selectionne et execute le reader.

        :param path: Chemin du fichier.
        :param file_type: Type detecte.
        :param schema_id: Identifiant de schema.
        :param inspection: Inspection enrichie (fallback warnings).
        :returns: Records, erreurs et warnings.
        """
        if file_type is ImportFileType.INCOMING_CALLS:
            incoming = self._incoming.read(path)
            return (
                (*incoming.calls, *incoming.segments),
                incoming.errors,
                incoming.warnings,
            )
        if file_type is ImportFileType.OUTGOING_CALLS:
            outgoing = self._outgoing.read(path)
            return (
                (*outgoing.calls, *outgoing.segments),
                outgoing.errors,
                outgoing.warnings,
            )
        if file_type is ImportFileType.TICKETS:
            tickets = self._tickets.read(path)
            return (tuple(tickets.tickets), tickets.errors, tickets.warnings)
        if file_type is ImportFileType.AGENT_ACTIVITIES:
            if schema_id == "activities_wide":
                wide = self._activities_wide.read(path)
                return (tuple(wide.activities), wide.errors, wide.warnings)
            if schema_id == "activities_long":
                long = self._activities_long.read(path)
                return (tuple(long.activities), long.errors, long.warnings)
            return (
                (),
                (
                    ImportError.create(
                        code="SCHEMA_ACTIVITIES_UNSUPPORTED",
                        message=(f"schema activites agents non supporte: {schema_id}"),
                    ),
                ),
                inspection.warnings,
            )
        return (
            (),
            (
                ImportError.create(
                    code="FILE_TYPE_UNKNOWN",
                    message=f"type de fichier non gere: {file_type.value}",
                ),
            ),
            inspection.warnings,
        )

    @staticmethod
    def _metadata_from_inspection(inspection: FileInspection) -> FileMetadata:
        """Construit les metadonnees fichier depuis l'inspection.

        :param inspection: Inspection enrichie.
        :returns: Metadonnees pour ``ParseResult``.
        """
        return FileMetadata(
            path=inspection.path,
            encoding=inspection.encoding,
            separator=inspection.separator,
            sha256=inspection.sha256,
            detected_type=inspection.detected_type,
            schema_version=inspection.schema_version,
            row_count=max(0, inspection.lines_read - 1),
            column_names=inspection.raw_columns,
        )

    @staticmethod
    def _from_detection_error(path: Path, exc: FileDetectionError) -> ParseResult:
        """Convertit une erreur de detection en ``ParseResult`` FATAL.

        :param path: Chemin demande.
        :param exc: Exception de detection.
        :returns: Resultat sans enregistrements.
        """
        metadata = FileMetadata(
            path=str(path),
            encoding="?",
            separator=";",
            sha256=_EMPTY_SHA256,
            detected_type=ImportFileType.UNKNOWN,
            schema_version=SchemaVersion.UNKNOWN,
            row_count=0,
            column_names=(),
        )
        return ParseResult.build(
            file_metadata=metadata,
            errors=(
                ImportError.create(
                    code=exc.code,
                    message=exc.message,
                    severity=ImportSeverity.FATAL,
                ),
            ),
        )
