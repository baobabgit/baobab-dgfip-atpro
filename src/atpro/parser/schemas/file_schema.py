"""Definition d'un schema CSV reconnu.

:spec: FEAT-002.3
"""

from __future__ import annotations

from dataclasses import dataclass

from atpro.domain.enums.import_file_type import ImportFileType
from atpro.domain.enums.schema_version import SchemaVersion
from atpro.domain.exceptions.domain_error import DomainError


@dataclass(frozen=True, slots=True)
class FileSchema:
    """Signature de colonnes pour un type / variante de fichier.

    :param schema_id: Identifiant stable (ex. ``tickets_long``).
    :param file_type: Type metier detecte.
    :param schema_version: Version de schema.
    :param required_columns: Colonnes normalisees obligatoires.
    :param optional_columns: Colonnes normalisees optionnelles (bonus).
    :param filename_hints: Sous-chaines de nom (indice faible uniquement).
    :spec: FEAT-002.3
    """

    schema_id: str
    file_type: ImportFileType
    schema_version: SchemaVersion
    required_columns: frozenset[str]
    optional_columns: frozenset[str] = frozenset()
    filename_hints: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        """Valide la definition.

        :raises DomainError: Si la signature est invalide.
        """
        if not self.schema_id.strip():
            raise DomainError("FileSchema.schema_id obligatoire")
        if not self.required_columns:
            raise DomainError("FileSchema.required_columns obligatoire")
