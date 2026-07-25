"""Apercu limite d'un parsing.

:spec: FEAT-003.1
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from atpro.parser.results.file_metadata import FileMetadata
from atpro.parser.results.import_error import ImportError
from atpro.parser.results.import_warning import ImportWarning


@dataclass(frozen=True, slots=True)
class ParsePreview:
    """Apercu des premiers enregistrements d'un fichier.

    :param file_metadata: Metadonnees fichier.
    :param limit: Limite demandee.
    :param records: Enregistrements previsualises.
    :param warnings: Avertissements observes.
    :param errors: Erreurs observees.
    :spec: FEAT-003.1
    """

    file_metadata: FileMetadata
    limit: int
    records: tuple[Any, ...]
    warnings: tuple[ImportWarning, ...]
    errors: tuple[ImportError, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialise l'apercu.

        :returns: Dictionnaire JSON-compatible.
        """
        return {
            "file_metadata": self.file_metadata.to_dict(),
            "limit": self.limit,
            "record_count": len(self.records),
            "warnings": [warning.to_dict() for warning in self.warnings],
            "errors": [error.to_dict() for error in self.errors],
        }

    def to_json(self) -> str:
        """Serialise en JSON stable.

        :returns: Chaine JSON.
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True)
