"""Tests d'inspection du schema metier importe.

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


class TestBusinessTablesSchema:
    def _upgrade(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> str:
        db_path = tmp_path / "schema029.db"
        url = f"sqlite:///{db_path.as_posix()}"
        monkeypatch.setenv("ATPRO_DATABASE_URL", url)
        config = AlembicConfigFactory().create(
            settings=DatabaseSettings(database_url=url)
        )
        command.upgrade(config, "head")
        return url

    def test_FEAT_017_2_tables_metier_presentes(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        url = self._upgrade(tmp_path, monkeypatch)
        engine = create_engine(url)
        try:
            names = set(inspect(engine).get_table_names())
            assert {
                "calls",
                "call_segments",
                "tickets",
                "agent_daily_activities",
            }.issubset(names)
        finally:
            engine.dispose()

    def test_FEAT_017_2_contraintes_uniques_metier(
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

            assert ("source_system", "external_call_id") in unique_cols("calls")
            assert ("call_id", "segment_index") in unique_cols("call_segments")
            assert ("source_system", "external_ticket_id") in unique_cols("tickets")
            assert ("raw_agent_name", "activity_date", "line_fingerprint") in (
                unique_cols("agent_daily_activities")
            )
        finally:
            engine.dispose()

    def test_FEAT_017_2_types_durees_entiers(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        url = self._upgrade(tmp_path, monkeypatch)
        engine = create_engine(url)
        try:
            cols = {
                c["name"]: c["type"]
                for c in inspect(engine).get_columns("call_segments")
            }
            assert "INTEGER" in str(cols["talk_duration_seconds"]).upper()
            assert "INTEGER" in str(cols["hold_duration_seconds"]).upper()
            activity_cols = {
                c["name"]: c["type"]
                for c in inspect(engine).get_columns("agent_daily_activities")
            }
            assert "DATE" in str(activity_cols["activity_date"]).upper()
        finally:
            engine.dispose()

    def test_FEAT_017_2_modeles_metier_sur_metadata(self) -> None:
        names = set(Base.metadata.tables)
        assert "calls" in names
        assert "call_segments" in names
        assert "tickets" in names
        assert "agent_daily_activities" in names
