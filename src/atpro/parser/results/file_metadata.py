"""Metadonnees d'un fichier importe.

:spec: FEAT-003.1
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from atpro.domain.enums.import_file_type import ImportFileType
from atpro.domain.enums.schema_version import SchemaVersion
from atpro.domain.exceptions.domain_error import DomainError
from atpro.domain.value_objects.file_sha256 import FileSha256


@dataclass(frozen=True, slots=True)
class FileMetadata:
    """Metadonnees detectees sur un fichier CSV.

    :param path: Chemin source.
    :param encoding: Encodage detecte.
    :param separator: Separateur detecte.
    :param sha256: Empreinte du contenu.
    :param detected_type: Type de fichier detecte.
    :param schema_version: Version de schema.
    :param row_count: Nombre de lignes de donnees.
    :param column_names: Colonnes observees.
    :spec: FEAT-003.1
    """

    path: str
    encoding: str
    separator: str
    sha256: FileSha256
    detected_type: ImportFileType
    schema_version: SchemaVersion
    row_count: int
    column_names: tuple[str, ...]

    def __post_init__(self) -> None:
        """Valide les champs obligatoires.

        :raises DomainError: Si un champ est invalide.
        """
        if not self.path.strip():
            raise DomainError("FileMetadata.path obligatoire")
        if not self.encoding.strip():
            raise DomainError("FileMetadata.encoding obligatoire")
        if not self.separator:
            raise DomainError("FileMetadata.separator obligatoire")
        if self.row_count < 0:
            raise DomainError("FileMetadata.row_count negatif")

    @classmethod
    def from_path(
        cls,
        path: Path,
        *,
        encoding: str,
        separator: str,
        sha256: FileSha256,
        detected_type: ImportFileType,
        schema_version: SchemaVersion,
        row_count: int,
        column_names: tuple[str, ...],
    ) -> FileMetadata:
        """Cree les metadonnees depuis un chemin.

        :returns: Instance valide.
        """
        return cls(
            path=str(path),
            encoding=encoding,
            separator=separator,
            sha256=sha256,
            detected_type=detected_type,
            schema_version=schema_version,
            row_count=row_count,
            column_names=column_names,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialise les metadonnees.

        :returns: Dictionnaire JSON-compatible.
        """
        payload = asdict(self)
        payload["sha256"] = self.sha256.value
        payload["detected_type"] = self.detected_type.value
        payload["schema_version"] = self.schema_version.value
        payload["column_names"] = list(self.column_names)
        return payload
