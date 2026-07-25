"""Reader CSV des tickets.

:spec: FEAT-007.1
"""

from __future__ import annotations

import csv
from collections.abc import Sequence
from io import StringIO
from pathlib import Path

from atpro.domain.enums.import_file_type import ImportFileType
from atpro.parser.detection.file_inspector import FileInspector
from atpro.parser.results.import_error import ImportError
from atpro.parser.results.import_warning import ImportWarning
from atpro.parser.schemas.schema_detector import SchemaDetector
from atpro.parser.tickets.raw_ticket_row import RawTicketRow
from atpro.parser.tickets.ticket_builder import TicketBuilder
from atpro.parser.tickets.ticket_field_mapper import TicketFieldMapper
from atpro.parser.tickets.ticket_import_result import TicketImportResult


class TicketsReader:
    """Parse un fichier tickets (schema long ou reduit).

    :spec: FEAT-007.1
    """

    _ACCEPTED_SCHEMAS = frozenset({"tickets_long", "tickets_reduced"})

    def __init__(
        self,
        *,
        inspector: FileInspector | None = None,
        mapper: TicketFieldMapper | None = None,
        builder: TicketBuilder | None = None,
        schema_detector: SchemaDetector | None = None,
    ) -> None:
        """Injecte les collaborateurs.

        :param inspector: Inspection fichier.
        :param mapper: Mapping colonnes.
        :param builder: Construction Ticket.
        :param schema_detector: Detection schema.
        """
        self._inspector = inspector or FileInspector()
        self._mapper = mapper or TicketFieldMapper()
        self._builder = builder or TicketBuilder()
        self._schemas = schema_detector or SchemaDetector()

    def read(self, path: Path) -> TicketImportResult:
        """Lit et construit les tickets.

        :param path: Chemin du fichier.
        :returns: Tickets et diagnostics.
        :raises FileDetectionError: Fichier absent ou vide.
        :spec: FEAT-007.1
        """
        inspection = self._inspector.inspect(path)
        schema_match = self._schemas.detect(
            inspection.normalized_columns,
            file_name=path.name,
            already_normalized=True,
        )
        pre_errors: list[ImportError] = []
        pre_warnings: list[ImportWarning] = list(schema_match.warnings)
        pre_warnings.extend(inspection.warnings)

        if schema_match.file_type not in {
            ImportFileType.TICKETS,
            ImportFileType.UNKNOWN,
        }:
            pre_warnings.append(
                ImportWarning.create(
                    code="SCHEMA_NOT_TICKETS",
                    message=(
                        "schema detecte different de tickets: "
                        f"{schema_match.schema_id}"
                    ),
                )
            )
        elif schema_match.schema_id in self._ACCEPTED_SCHEMAS:
            pass
        elif schema_match.schema_id == "unknown":
            pre_errors.append(
                ImportError.create(
                    code="SCHEMA_TICKETS_REQUIRED",
                    message="colonnes incompatibles avec un schema tickets connu",
                )
            )

        text = path.read_text(encoding=inspection.encoding)
        dict_reader = csv.DictReader(StringIO(text), delimiter=inspection.separator)
        raw_rows: list[RawTicketRow] = []
        for index, row in enumerate(dict_reader, start=2):
            cells = {
                (key or ""): (value or "")
                for key, value in row.items()
                if key is not None
            }
            raw_rows.append(self._mapper.map_row(index, cells))

        built = self._builder.build(raw_rows)
        return TicketImportResult(
            tickets=built.tickets,
            agent_identities=built.agent_identities,
            site_identities=built.site_identities,
            errors=tuple(pre_errors) + built.errors,
            warnings=tuple(pre_warnings) + built.warnings,
        )

    def read_rows(
        self, rows: Sequence[dict[str, str]], *, start_row_number: int = 2
    ) -> TicketImportResult:
        """Construit des tickets depuis des lignes deja chargees.

        :param rows: Dictionnaires colonnes → valeurs.
        :param start_row_number: Premiere ligne de donnees.
        :returns: Resultat d'import.
        """
        raw_rows = [
            self._mapper.map_row(start_row_number + offset, row)
            for offset, row in enumerate(rows)
        ]
        headers = tuple(rows[0].keys()) if rows else ()
        schema_match = self._schemas.detect(headers, already_normalized=False)
        pre_warnings = list(schema_match.warnings)
        if schema_match.file_type is ImportFileType.TICKETS:
            pass
        elif schema_match.schema_id != "unknown":
            pre_warnings.append(
                ImportWarning.create(
                    code="SCHEMA_NOT_TICKETS",
                    message=f"schema detecte: {schema_match.schema_id}",
                )
            )
        built = self._builder.build(raw_rows)
        return TicketImportResult(
            tickets=built.tickets,
            agent_identities=built.agent_identities,
            site_identities=built.site_identities,
            errors=built.errors,
            warnings=tuple(pre_warnings) + built.warnings,
        )
