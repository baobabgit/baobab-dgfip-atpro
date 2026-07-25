"""Localisation optionnelle des CSV reels de reference.

:spec: FEAT-013.1
"""

from __future__ import annotations

import os
from collections.abc import Iterator, Mapping
from pathlib import Path


class ReferenceDataLocator:
    """Lit ``ATPRO_REFERENCE_CSV_DIR`` et expose les CSV de reference.

    Helper de test / validation locale. Ne fait pas partie du contrat public
    de la librairie (package ``atpro.testing``).

    :param env: Mapping d'environnement (injectable pour les tests).
    :spec: FEAT-013.1
    """

    ENV_VAR: str = "ATPRO_REFERENCE_CSV_DIR"

    def __init__(self, *, env: Mapping[str, str] | None = None) -> None:
        """Initialise le localisateur.

        :param env: Environnement a lire ; ``os.environ`` par defaut.
        """
        self._env: Mapping[str, str] = env if env is not None else os.environ

    def resolve_dir(self) -> Path | None:
        """Retourne le dossier configure, ou ``None`` si absent.

        :returns: Chemin absolu du dossier, ou ``None`` si la variable est
            absente ou vide.
        """
        raw = self._env.get(self.ENV_VAR)
        if raw is None:
            return None
        stripped = raw.strip()
        if not stripped:
            return None
        return Path(stripped).expanduser().resolve()

    def is_configured(self) -> bool:
        """Indique si ``ATPRO_REFERENCE_CSV_DIR`` pointe vers un chemin.

        :returns: ``True`` si un chemin non vide est configure.
        """
        return self.resolve_dir() is not None

    def is_empty(self) -> bool:
        """Indique si le dossier configure ne contient aucun ``*.csv``.

        Si la variable n'est pas configuree, le dossier est considere vide
        (aucun fichier de reference disponible).

        :returns: ``True`` si aucun CSV n'est enumerable.
        """
        directory = self.resolve_dir()
        if directory is None:
            return True
        if not directory.is_dir():
            return True
        return next(self.iter_csv_files(), None) is None

    def iter_csv_files(self) -> Iterator[Path]:
        """Itere les fichiers ``*.csv`` du dossier de reference.

        :returns: Iterateur trie par nom de fichier.
        :yields: Chemins absolus des CSV.
        """
        directory = self.resolve_dir()
        if directory is None or not directory.is_dir():
            return
        yield from sorted(directory.glob("*.csv"))
