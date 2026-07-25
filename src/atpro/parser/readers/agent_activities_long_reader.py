"""Reader CSV des activites agents (format long).

:spec: FEAT-009.1
"""

from __future__ import annotations

import csv
from collections.abc import Sequence
from datetime import date
from io import StringIO
from pathlib import Path

from atpro.domain.enums.import_file_type import ImportFileType
from atpro.parser.activities.activity_accumulator import ActivityAccumulator
from atpro.parser.activities.activity_builder import ActivityBuilder
from atpro.parser.activities.activity_import_result import ActivityImportResult
from atpro.parser.detection.file_inspector import FileInspector
from atpro.parser.results.import_error import ImportError
from atpro.parser.results.import_warning import ImportWarning
from atpro.parser.schemas.schema_detector import SchemaDetector


class AgentActivitiesLongReader:
    """Parse un fichier d'activites agents en format long.

    Une ligne = une mesure ; regroupement par date et agent.

    :spec: FEAT-009.1
    """

    _EXPECTED_SCHEMA = "activities_long"

    def __init__(
        self,
        *,
        inspector: FileInspector | None = None,
        builder: ActivityBuilder | None = None,
        schema_detector: SchemaDetector | None = None,
    ) -> None:
        """Injecte les collaborateurs.

        :param inspector: Inspection fichier.
        :param builder: Construction d'activites.
        :param schema_detector: Detection schema.
        """
        self._inspector = inspector or FileInspector()
        self._builder = builder or ActivityBuilder()
        self._schemas = schema_detector or SchemaDetector()

    def read(self, path: Path) -> ActivityImportResult:
        """Lit et construit les activites.

        :param path: Chemin du fichier.
        :returns: Activites et diagnostics.
        :raises FileDetectionError: Fichier absent ou vide.
        :spec: FEAT-009.1
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
        self._check_schema(
            schema_match.file_type,
            schema_match.schema_id,
            pre_errors,
            pre_warnings,
        )

        text = path.read_text(encoding=inspection.encoding)
        dict_reader = csv.DictReader(StringIO(text), delimiter=inspection.separator)
        rows: list[dict[str, str]] = []
        for row in dict_reader:
            cells = {
                (key or ""): (value or "")
                for key, value in row.items()
                if key is not None
            }
            rows.append(cells)

        built = self._build_from_rows(rows, start_row_number=2)
        return ActivityImportResult(
            activities=built.activities,
            errors=tuple(pre_errors) + built.errors,
            warnings=tuple(pre_warnings) + built.warnings,
        )

    def read_rows(
        self, rows: Sequence[dict[str, str]], *, start_row_number: int = 2
    ) -> ActivityImportResult:
        """Construit des activites depuis des lignes deja chargees.

        :param rows: Dictionnaires colonnes → valeurs.
        :param start_row_number: Premiere ligne de donnees.
        :returns: Resultat d'import.
        :spec: FEAT-009.1
        """
        headers = tuple(rows[0].keys()) if rows else ()
        schema_match = self._schemas.detect(headers, already_normalized=False)
        pre_errors: list[ImportError] = []
        pre_warnings = list(schema_match.warnings)
        self._check_schema(
            schema_match.file_type,
            schema_match.schema_id,
            pre_errors,
            pre_warnings,
            for_rows=True,
        )
        built = self._build_from_rows(rows, start_row_number=start_row_number)
        return ActivityImportResult(
            activities=built.activities,
            errors=tuple(pre_errors) + built.errors,
            warnings=tuple(pre_warnings) + built.warnings,
        )

    def _build_from_rows(
        self, rows: Sequence[dict[str, str]], *, start_row_number: int
    ) -> ActivityImportResult:
        """Pipeline interne format long avec regroupement.

        :param rows: Lignes.
        :param start_row_number: Offset.
        :returns: Resultat partiel.
        """
        grouped: dict[tuple[date, str], ActivityAccumulator] = {}
        order: list[tuple[date, str]] = []
        pre_errors: list[ImportError] = []
        pre_warnings: list[ImportWarning] = []

        for offset, cells in enumerate(rows):
            row_number = start_row_number + offset
            periode = self._builder.cell(cells, "periode")
            agent = self._builder.cell(cells, "agent_groupe_agent")
            measure_name = self._builder.cell(cells, "noms_de_mesures")
            measure_raw = self._builder.raw_cell(cells, "valeurs_de_mesures")
            measure_value = "" if measure_raw is None else measure_raw

            group = None
            if periode is not None and agent is not None:
                group = self._builder.group_key(periode_raw=periode, agent_raw=agent)

            if group is None:
                _acc, errs, warns = self._builder.create_accumulator(
                    periode_raw=periode,
                    agent_raw=agent,
                    row_number=row_number,
                )
                pre_errors.extend(errs)
                pre_warnings.extend(warns)
                continue

            if group not in grouped:
                acc, errs, warns = self._builder.create_accumulator(
                    periode_raw=periode,
                    agent_raw=agent,
                    row_number=row_number,
                )
                pre_errors.extend(errs)
                pre_warnings.extend(warns)
                if acc is None:
                    continue
                grouped[group] = acc
                order.append(group)
            else:
                grouped[group].note_row(row_number)

            self._builder.apply_long_measure(
                grouped[group],
                measure_name=measure_name,
                measure_value=measure_value,
                row_number=row_number,
            )

        accumulators = [grouped[key] for key in order]
        built = self._builder.build(accumulators)
        return ActivityImportResult(
            activities=built.activities,
            errors=tuple(pre_errors) + built.errors,
            warnings=tuple(pre_warnings) + built.warnings,
        )

    def _check_schema(
        self,
        file_type: ImportFileType,
        schema_id: str,
        errors: list[ImportError],
        warnings: list[ImportWarning],
        *,
        for_rows: bool = False,
    ) -> None:
        """Valide le schema detecte pour le format long.

        :param file_type: Type detecte.
        :param schema_id: Identifiant schema.
        :param errors: Accumulateur erreurs.
        :param warnings: Accumulateur warnings.
        :param for_rows: Mode ``read_rows``.
        """
        if file_type not in {
            ImportFileType.AGENT_ACTIVITIES,
            ImportFileType.UNKNOWN,
        }:
            warnings.append(
                ImportWarning.create(
                    code="SCHEMA_NOT_ACTIVITIES",
                    message=(
                        "schema detecte different d'activites agents: " f"{schema_id}"
                    ),
                )
            )
            return
        if schema_id == self._EXPECTED_SCHEMA:
            return
        if schema_id == "unknown":
            if for_rows and file_type is ImportFileType.UNKNOWN:
                return
            errors.append(
                ImportError.create(
                    code="SCHEMA_ACTIVITIES_LONG_REQUIRED",
                    message=(
                        "colonnes incompatibles avec le schema "
                        f"{self._EXPECTED_SCHEMA}"
                    ),
                )
            )
            return
        warnings.append(
            ImportWarning.create(
                code="SCHEMA_NOT_ACTIVITIES_LONG",
                message=(
                    f"schema detecte: {schema_id} " f"(attendu {self._EXPECTED_SCHEMA})"
                ),
            )
        )
