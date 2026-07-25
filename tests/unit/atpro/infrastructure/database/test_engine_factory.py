"""Tests unitaires de ``EngineFactory``.

:spec: FEAT-016.1
"""

from __future__ import annotations

from sqlalchemy.engine import Engine

from atpro.infrastructure.config.database_settings import DatabaseSettings
from atpro.infrastructure.database.engine_factory import EngineFactory


class TestEngineFactory:
    def test_FEAT_016_1_creation_engine_url_valide(self) -> None:
        settings = DatabaseSettings(
            database_url="postgresql+psycopg://u:p@localhost:5432/atpro"
        )
        engine = EngineFactory().create(settings)
        assert isinstance(engine, Engine)
        assert engine.url.drivername == "postgresql+psycopg"
        assert engine.url.database == "atpro"
        engine.dispose()
