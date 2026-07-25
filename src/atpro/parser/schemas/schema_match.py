"""Resultat du scoring d'un schema.

:spec: FEAT-002.3
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from atpro.domain.enums.import_file_type import ImportFileType
from atpro.domain.enums.schema_version import SchemaVersion
from atpro.parser.results.import_warning import ImportWarning


@dataclass(frozen=True, slots=True)
class SchemaMatch:
    """Meilleure detection de schema pour un jeu de colonnes.

    :param schema_id: Identifiant du schema retenu (``unknown`` si aucun).
    :param file_type: Type detecte.
    :param schema_version: Version detectee.
    :param score: Score brut de correspondance.
    :param confidence: Confiance normalisee ``[0, 1]``.
    :param matched_required: Colonnes obligatoires presentes.
    :param missing_required: Colonnes obligatoires absentes.
    :param extra_columns: Colonnes presentes hors signature.
    :param warnings: Avertissements (colonnes manquantes, ambiguite…).
    :spec: FEAT-002.3
    """

    schema_id: str
    file_type: ImportFileType
    schema_version: SchemaVersion
    score: float
    confidence: float
    matched_required: tuple[str, ...]
    missing_required: tuple[str, ...]
    extra_columns: tuple[str, ...]
    warnings: tuple[ImportWarning, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialise le match.

        :returns: Dictionnaire JSON-compatible.
        """
        payload = asdict(self)
        payload["file_type"] = self.file_type.value
        payload["schema_version"] = self.schema_version.value
        payload["matched_required"] = list(self.matched_required)
        payload["missing_required"] = list(self.missing_required)
        payload["extra_columns"] = list(self.extra_columns)
        payload["warnings"] = [warning.to_dict() for warning in self.warnings]
        return payload
