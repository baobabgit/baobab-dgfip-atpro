"""Fabrique d'engine SQLAlchemy a partir de la configuration.

:spec: FEAT-016.1
"""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from atpro.infrastructure.config.database_settings import DatabaseSettings


class EngineFactory:
    """Cree un :class:`~sqlalchemy.engine.Engine` sans connexion a l'import.

    :spec: FEAT-016.1
    """

    def create(
        self,
        settings: DatabaseSettings,
        *,
        echo: bool = False,
    ) -> Engine:
        """Construit un engine depuis :class:`DatabaseSettings`.

        La connexion reseau n'est etablie qu'au premier usage (checkout pool).

        :param settings: Configuration PostgreSQL injectee.
        :param echo: Active le journal SQL si ``True``.
        :returns: Engine SQLAlchemy 2.x.
        :rtype: Engine
        """
        return create_engine(
            settings.sqlalchemy_url(),
            echo=echo,
            pool_pre_ping=True,
        )
