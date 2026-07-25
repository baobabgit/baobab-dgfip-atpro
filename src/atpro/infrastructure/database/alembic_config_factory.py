"""Fabrique de configuration Alembic branchee sur DatabaseSettings.

:spec: FEAT-017.1
"""

from __future__ import annotations

from pathlib import Path

from alembic.config import Config

from atpro.infrastructure.config.database_settings import DatabaseSettings


class AlembicConfigFactory:
    """Construit une ``Config`` Alembic sans chemin absolu local.

    :spec: FEAT-017.1
    """

    def create(
        self,
        *,
        ini_path: Path | str | None = None,
        settings: DatabaseSettings | None = None,
    ) -> Config:
        """Charge ``alembic.ini`` et injecte l'URL SQLAlchemy du projet.

        :param ini_path: Chemin vers ``alembic.ini`` (defaut : CWD).
        :param settings: Configuration injectee (defaut : environnement).
        :returns: Configuration Alembic prete a l'emploi.
        :rtype: Config
        """
        resolved = Path(ini_path) if ini_path is not None else Path("alembic.ini")
        config = Config(str(resolved))
        database_settings = settings if settings is not None else DatabaseSettings()
        config.set_main_option(
            "sqlalchemy.url",
            database_settings.sqlalchemy_url(),
        )
        return config
