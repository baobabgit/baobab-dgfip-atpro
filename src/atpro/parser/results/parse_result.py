"""Resultat complet d'un parsing.

:spec: FEAT-003.1
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from atpro.domain.enums.import_file_type import ImportFileType
from atpro.domain.enums.import_severity import ImportSeverity
from atpro.domain.enums.parse_status import ParseStatus
from atpro.domain.enums.schema_version import SchemaVersion
from atpro.parser.results.file_metadata import FileMetadata
from atpro.parser.results.import_error import ImportError
from atpro.parser.results.import_warning import ImportWarning
from atpro.parser.results.parse_summary import ParseSummary


@dataclass(frozen=True, slots=True)
class ParseResult:
    """Resultat standard retourne par les readers.

    :param file_metadata: Metadonnees fichier.
    :param detected_type: Type detecte.
    :param schema_version: Version de schema.
    :param records: Enregistrements metier produits.
    :param warnings: Avertissements.
    :param errors: Erreurs.
    :param summary: Resume quantitatif.
    :spec: FEAT-003.1
    """

    file_metadata: FileMetadata
    detected_type: ImportFileType
    schema_version: SchemaVersion
    records: tuple[Any, ...]
    warnings: tuple[ImportWarning, ...]
    errors: tuple[ImportError, ...]
    summary: ParseSummary

    @classmethod
    def build(
        cls,
        *,
        file_metadata: FileMetadata,
        records: tuple[Any, ...] = (),
        warnings: tuple[ImportWarning, ...] = (),
        errors: tuple[ImportError, ...] = (),
    ) -> ParseResult:
        """Construit un resultat avec resume derive.

        :returns: ParseResult coherent.
        """
        if errors:
            has_fatal = any(
                err.issue.severity is ImportSeverity.FATAL for err in errors
            )
            status = (
                ParseStatus.FAILED if has_fatal or not records else ParseStatus.PARTIAL
            )
        elif warnings and not records:
            status = ParseStatus.PARTIAL
        else:
            status = ParseStatus.SUCCESS
        summary = ParseSummary(
            status=status,
            record_count=len(records),
            warning_count=len(warnings),
            error_count=len(errors),
        )
        return cls(
            file_metadata=file_metadata,
            detected_type=file_metadata.detected_type,
            schema_version=file_metadata.schema_version,
            records=records,
            warnings=warnings,
            errors=errors,
            summary=summary,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialise le resultat (sans les records metier bruts).

        :returns: Dictionnaire JSON-compatible stable.
        """
        return {
            "file_metadata": self.file_metadata.to_dict(),
            "detected_type": self.detected_type.value,
            "schema_version": self.schema_version.value,
            "record_count": len(self.records),
            "warnings": [warning.to_dict() for warning in self.warnings],
            "errors": [error.to_dict() for error in self.errors],
            "summary": self.summary.to_dict(),
        }

    def to_json(self) -> str:
        """Serialise en JSON stable (cles triees).

        :returns: Chaine JSON.
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True)
