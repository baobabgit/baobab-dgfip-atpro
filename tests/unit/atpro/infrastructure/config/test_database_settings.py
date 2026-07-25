"""Tests unitaires de ``DatabaseSettings``.

:spec: FEAT-015.2
"""

from __future__ import annotations

import pytest

from atpro.infrastructure.config.database_configuration_error import (
    DatabaseConfigurationError,
)
from atpro.infrastructure.config.database_settings import DatabaseSettings


class TestDatabaseSettings:
    def test_FEAT_015_2_url_explicite(self) -> None:
        settings = DatabaseSettings(
            database_url="postgresql+psycopg://u:secret@db:5432/app"
        )
        assert settings.sqlalchemy_url() == (
            "postgresql+psycopg://u:secret@db:5432/app"
        )

    def test_FEAT_015_2_url_vide_normalisee_en_none(self) -> None:
        settings = DatabaseSettings(database_url="   ")
        assert settings.database_url is None
        assert "localhost" in settings.sqlalchemy_url()

    def test_FEAT_015_2_assemblage_composants(self) -> None:
        settings = DatabaseSettings(
            database_url=None,
            database_host="localhost",
            database_port=5433,
            database_name="atpro_test",
            database_user="tester",
            database_password="s3cret",
        )
        assert settings.sqlalchemy_url() == (
            "postgresql+psycopg://tester:s3cret@localhost:5433/atpro_test"
        )

    def test_FEAT_015_2_erreur_composants_manquants(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("ATPRO_DATABASE_URL", raising=False)
        settings = DatabaseSettings(
            database_url=None,
            database_host="",
            database_name="atpro",
            database_user="atpro",
            database_password="atpro",
        )
        with pytest.raises(DatabaseConfigurationError, match="manquantes"):
            settings.sqlalchemy_url()

    def test_FEAT_015_2_masquage_mot_de_passe(self) -> None:
        settings = DatabaseSettings(
            database_url="postgresql+psycopg://u:s3cret@db:5432/app"
        )
        masked = settings.masked_sqlalchemy_url()
        assert "s3cret" not in masked
        assert "***" in masked
        assert "s3cret" not in repr(settings)

    def test_FEAT_015_2_repr_si_non_configure(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("ATPRO_DATABASE_URL", raising=False)
        settings = DatabaseSettings(
            database_url=None,
            database_host="",
            database_name="",
            database_user="",
            database_password="",
        )
        assert "unconfigured" in repr(settings)
