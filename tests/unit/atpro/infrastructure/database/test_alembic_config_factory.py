"""Tests unitaires Alembic / ``AlembicConfigFactory``.

:spec: FEAT-017.1
"""

from __future__ import annotations

from pathlib import Path

import pytest
from alembic import command
from alembic.script import ScriptDirectory

from atpro.infrastructure.config.database_settings import DatabaseSettings
from atpro.infrastructure.database.alembic_config_factory import AlembicConfigFactory
from atpro.infrastructure.database.base import Base


class TestAlembicConfigFactory:
    def test_FEAT_017_1_detecte_configuration(self) -> None:
        config = AlembicConfigFactory().create(
            settings=DatabaseSettings(
                database_url="sqlite:///:memory:",
            )
        )
        assert "migrations" in config.get_main_option("script_location")
        assert config.get_main_option("sqlalchemy.url") == "sqlite:///:memory:"

    def test_FEAT_017_1_metadata_sqlalchemy_importable(self) -> None:
        assert Base.metadata is not None
        assert Base.metadata.naming_convention is not None

    def test_FEAT_017_1_upgrade_head_et_downgrade_base(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        db_path = tmp_path / "alembic_test.db"
        url = f"sqlite:///{db_path.as_posix()}"
        monkeypatch.setenv("ATPRO_DATABASE_URL", url)
        settings = DatabaseSettings(database_url=url)
        config = AlembicConfigFactory().create(settings=settings)
        script = ScriptDirectory.from_config(config)
        assert script.get_current_head() == "20260726_baseline"

        command.upgrade(config, "head")
        command.downgrade(config, "base")
