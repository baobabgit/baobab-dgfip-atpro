"""Tests d'inspection du schema imports/referentiels.

:spec: FEAT-017.2
"""

from __future__ import annotations

from pathlib import Path

import pytest
from alembic import command
from sqlalchemy import create_engine, inspect

from atpro.infrastructure.config.database_settings import DatabaseSettings
from atpro.infrastructure.database import models as _models  # noqa: F401
from atpro.infrastructure.database.alembic_config_factory import AlembicConfigFactory
from atpro.infrastructure.database.base import Base


class TestImportsReferentielsSchema:
    def _upgrade(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> str:
        db_path = tmp_path / "schema028.db"
        url = f"sqlite:///{db_path.as_posix()}"
        monkeypatch.setenv("ATPRO_DATABASE_URL", url)
        config = AlembicConfigFactory().create(
            settings=DatabaseSettings(database_url=url)
        )
        command.upgrade(config, "head")
        return url

    def test_FEAT_017_2_migration_base_vide_cree_tables(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        url = self._upgrade(tmp_path, monkeypatch)
        engine = create_engine(url)
        try:
            names = set(inspect(engine).get_table_names())
            assert {
                "import_batches",
                "import_rejected_rows",
                "sites",
                "agents",
                "agent_aliases",
                "agent_site_assignments",
                "alembic_version",
            }.issubset(names)
        finally:
            engine.dispose()

    def test_FEAT_017_2_contraintes_uniques(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        url = self._upgrade(tmp_path, monkeypatch)
        engine = create_engine(url)
        try:
            inspector = inspect(engine)

            def unique_cols(table: str) -> set[tuple[str, ...]]:
                return {
                    tuple(uc["column_names"])
                    for uc in inspector.get_unique_constraints(table)
                }

            assert ("sha256",) in unique_cols("import_batches")
            assert ("normalized_name",) in unique_cols("sites")
            assert ("code",) in unique_cols("sites")
            assert ("normalized_identity",) in unique_cols("agents")
            assert ("normalized_alias",) in unique_cols("agent_aliases")
            assert ("agent_id", "site_id", "start_date") in unique_cols(
                "agent_site_assignments"
            )
        finally:
            engine.dispose()

    def test_FEAT_017_2_foreign_keys_imports_rejets(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        url = self._upgrade(tmp_path, monkeypatch)
        engine = create_engine(url)
        try:
            inspector = inspect(engine)
            rejected_fks = inspector.get_foreign_keys("import_rejected_rows")
            assert any(
                fk["referred_table"] == "import_batches"
                and fk["constrained_columns"] == ["import_batch_id"]
                for fk in rejected_fks
            )
            alias_fks = inspector.get_foreign_keys("agent_aliases")
            assert any(fk["referred_table"] == "agents" for fk in alias_fks)
            assignment_fks = inspector.get_foreign_keys("agent_site_assignments")
            referred = {fk["referred_table"] for fk in assignment_fks}
            assert {"agents", "sites"}.issubset(referred)
        finally:
            engine.dispose()

    def test_FEAT_017_2_modeles_orm_enregistres_sur_metadata(self) -> None:
        table_names = set(Base.metadata.tables)
        assert "import_batches" in table_names
        assert "sites" in table_names
        assert "agents" in table_names
        assert "agent_aliases" in table_names
        assert "agent_site_assignments" in table_names
        assert "import_rejected_rows" in table_names
