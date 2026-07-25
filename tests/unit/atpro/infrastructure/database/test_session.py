"""Tests unitaires de ``SessionFactory``.

:spec: FEAT-016.1
"""

from __future__ import annotations

import importlib

import pytest
from sqlalchemy import Integer, String, create_engine, select
from sqlalchemy.orm import Mapped, Session, mapped_column

from atpro.infrastructure.database.base import Base
from atpro.infrastructure.database.session import SessionFactory


class _SampleRow(Base):
    """Modele ORM minimal pour les tests de session."""

    __tablename__ = "bl025_sample_rows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    label: Mapped[str] = mapped_column(String(32), nullable=False)


class TestSessionFactory:
    def test_FEAT_016_1_creation_et_fermeture_session(self) -> None:
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine, tables=[_SampleRow.__table__])
        factory = SessionFactory(engine)

        session = factory.create_session()
        assert isinstance(session, Session)
        session.add(_SampleRow(label="opened"))
        session.commit()
        session.close()

        session = factory.create_session()
        labels = list(session.scalars(select(_SampleRow.label)))
        session.close()
        assert labels == ["opened"]
        engine.dispose()

    def test_FEAT_016_1_rollback_sur_exception(self) -> None:
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine, tables=[_SampleRow.__table__])
        factory = SessionFactory(engine)

        with pytest.raises(RuntimeError, match="boom"):
            with factory.session_scope() as session:
                session.add(_SampleRow(label="orphan"))
                session.flush()
                raise RuntimeError("boom")

        with factory.session_scope() as session:
            rows = session.scalars(select(_SampleRow)).all()
            assert rows == []
        engine.dispose()

    def test_FEAT_016_1_commit_sur_succes(self) -> None:
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine, tables=[_SampleRow.__table__])
        factory = SessionFactory(engine)

        with factory.session_scope() as session:
            session.add(_SampleRow(label="kept"))

        with factory.session_scope() as session:
            labels = [row.label for row in session.scalars(select(_SampleRow))]
            assert labels == ["kept"]
        engine.dispose()

    def test_FEAT_016_1_import_modules_sans_effet_reseau(self) -> None:
        module = importlib.import_module("atpro.infrastructure.database")
        assert module.Base is Base
        assert module.SessionFactory is SessionFactory
        assert module.EngineFactory is not None
