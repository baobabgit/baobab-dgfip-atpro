"""Reader CSV des appels sortants.

:spec: FEAT-006.1
"""

from __future__ import annotations

import csv
from collections.abc import Sequence
from io import StringIO
from pathlib import Path

from atpro.domain.enums.call_direction import CallDirection
from atpro.domain.enums.import_file_type import ImportFileType
from atpro.parser.calls.call_consolidation_result import CallConsolidationResult
from atpro.parser.calls.call_consolidator import CallConsolidator
from atpro.parser.calls.call_field_mapper import CallFieldMapper
from atpro.parser.calls.raw_call_row import RawCallRow
from atpro.parser.detection.file_inspector import FileInspector
from atpro.parser.results.import_error import ImportError
from atpro.parser.results.import_warning import ImportWarning
from atpro.parser.schemas.schema_detector import SchemaDetector


class OutgoingCallsReader:
    """Parse un fichier d'appels sortants vers ``Call`` / ``CallSegment``.

    :spec: FEAT-006.1
    """

    _EXPECTED_SCHEMA = "outgoing_calls_v1"

    def __init__(
        self,
        *,
        inspector: FileInspector | None = None,
        mapper: CallFieldMapper | None = None,
        consolidator: CallConsolidator | None = None,
        schema_detector: SchemaDetector | None = None,
    ) -> None:
        """Injecte les collaborateurs.

        :param inspector: Inspection fichier.
        :param mapper: Mapping colonnes.
        :param consolidator: Consolidation mesures.
        :param schema_detector: Detection schema.
        """
        self._inspector = inspector or FileInspector()
        self._mapper = mapper or CallFieldMapper()
        self._consolidator = consolidator or CallConsolidator()
        self._schemas = schema_detector or SchemaDetector()

    def read(self, path: Path) -> CallConsolidationResult:
        """Lit et consolide un fichier CSV sortant.

        :param path: Chemin du fichier.
        :returns: Appels, segments et diagnostics.
        :raises FileDetectionError: Fichier absent ou vide.
        :spec: FEAT-006.1
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
            ImportFileType.OUTGOING_CALLS,
            ImportFileType.UNKNOWN,
        }:
            pre_warnings.append(
                ImportWarning.create(
                    code="SCHEMA_NOT_OUTGOING",
                    message=(
                        "schema detecte different de appels sortants: "
                        f"{schema_match.schema_id}"
                    ),
                )
            )
        elif schema_match.schema_id == self._EXPECTED_SCHEMA:
            pass
        elif schema_match.schema_id == "unknown":
            pre_errors.append(
                ImportError.create(
                    code="SCHEMA_OUTGOING_REQUIRED",
                    message=(
                        "colonnes incompatibles avec le schema "
                        f"{self._EXPECTED_SCHEMA}"
                    ),
                )
            )

        text = path.read_text(encoding=inspection.encoding)
        dict_reader = csv.DictReader(StringIO(text), delimiter=inspection.separator)
        raw_rows: list[RawCallRow] = []
        for index, row in enumerate(dict_reader, start=2):
            cells = {
                (key or ""): (value or "")
                for key, value in row.items()
                if key is not None
            }
            raw_rows.append(self._mapper.map_row(index, cells))

        consolidated = self._consolidator.consolidate(
            raw_rows,
            direction=CallDirection.OUTGOING,
        )
        return CallConsolidationResult(
            calls=consolidated.calls,
            segments=consolidated.segments,
            errors=tuple(pre_errors) + consolidated.errors,
            warnings=tuple(pre_warnings) + consolidated.warnings,
        )

    def read_rows(
        self, rows: Sequence[dict[str, str]], *, start_row_number: int = 2
    ) -> CallConsolidationResult:
        """Consolide des lignes deja chargees (tests / orchestrateur).

        :param rows: Dictionnaires colonnes brutes → valeurs.
        :param start_row_number: Numero de la premiere ligne de donnees.
        :returns: Consolidation sortante.
        """
        raw_rows = [
            self._mapper.map_row(start_row_number + offset, row)
            for offset, row in enumerate(rows)
        ]
        headers = tuple(rows[0].keys()) if rows else ()
        schema_match = self._schemas.detect(headers, already_normalized=False)
        pre_warnings = list(schema_match.warnings)
        if schema_match.file_type is ImportFileType.OUTGOING_CALLS:
            pass
        elif schema_match.schema_id != "unknown":
            pre_warnings.append(
                ImportWarning.create(
                    code="SCHEMA_NOT_OUTGOING",
                    message=f"schema detecte: {schema_match.schema_id}",
                )
            )
        consolidated = self._consolidator.consolidate(
            raw_rows,
            direction=CallDirection.OUTGOING,
        )
        return CallConsolidationResult(
            calls=consolidated.calls,
            segments=consolidated.segments,
            errors=consolidated.errors,
            warnings=tuple(pre_warnings) + consolidated.warnings,
        )
