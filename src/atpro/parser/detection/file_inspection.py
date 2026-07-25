"""Resultat d'inspection bas niveau d'un fichier CSV.

:spec: FEAT-002.1
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from atpro.domain.enums.import_file_type import ImportFileType
from atpro.domain.enums.schema_version import SchemaVersion
from atpro.domain.exceptions.domain_error import DomainError
from atpro.domain.value_objects.file_sha256 import FileSha256
from atpro.parser.results.import_warning import ImportWarning


@dataclass(frozen=True, slots=True)
class FileInspection:
    """Metadonnees d'inspection sans parsing metier complet.

    :param path: Chemin original.
    :param file_name: Nom de fichier.
    :param size_bytes: Taille en octets.
    :param sha256: Empreinte du contenu exact.
    :param encoding: Encodage detecte.
    :param encoding_confidence: Confiance encodage ``[0, 1]``.
    :param separator: Separateur detecte.
    :param separator_confidence: Confiance separateur ``[0, 1]``.
    :param raw_columns: Colonnes brutes.
    :param normalized_columns: Colonnes normalisees.
    :param lines_read: Nombre de lignes lues (parcours binaire).
    :param detected_type: Type (UNKNOWN tant que BL-008 non branche).
    :param schema_version: Schema (UNKNOWN tant que BL-008 non branche).
    :param warnings: Avertissements non bloquants.
    :spec: FEAT-002.1
    """

    path: str
    file_name: str
    size_bytes: int
    sha256: FileSha256
    encoding: str
    encoding_confidence: float
    separator: str
    separator_confidence: float
    raw_columns: tuple[str, ...]
    normalized_columns: tuple[str, ...]
    lines_read: int
    detected_type: ImportFileType = ImportFileType.UNKNOWN
    schema_version: SchemaVersion = SchemaVersion.UNKNOWN
    warnings: tuple[ImportWarning, ...] = ()

    def __post_init__(self) -> None:
        """Valide les bornes minimales.

        :raises DomainError: Si un champ est incoherent.
        """
        if not self.path.strip():
            raise DomainError("FileInspection.path obligatoire")
        if self.size_bytes < 0:
            raise DomainError("FileInspection.size_bytes negatif")
        if not (0.0 <= self.encoding_confidence <= 1.0):
            raise DomainError("FileInspection.encoding_confidence hors bornes")
        if not (0.0 <= self.separator_confidence <= 1.0):
            raise DomainError("FileInspection.separator_confidence hors bornes")
        if self.lines_read < 0:
            raise DomainError("FileInspection.lines_read negatif")
        if len(self.raw_columns) != len(self.normalized_columns):
            raise DomainError(
                "FileInspection colonnes brutes/normalisees desynchronisees"
            )

    def to_dict(self) -> dict[str, Any]:
        """Serialise l'inspection.

        :returns: Dictionnaire JSON-compatible.
        """
        payload = asdict(self)
        payload["sha256"] = self.sha256.value
        payload["detected_type"] = self.detected_type.value
        payload["schema_version"] = self.schema_version.value
        payload["raw_columns"] = list(self.raw_columns)
        payload["normalized_columns"] = list(self.normalized_columns)
        payload["warnings"] = [warning.to_dict() for warning in self.warnings]
        return payload
