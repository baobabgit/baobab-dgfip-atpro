"""Tests unitaires de ``SqlAlchemyUnitOfWork``.

:spec: FEAT-016.2
"""

from __future__ import annotations

import pytest
from sqlalchemy import Integer, String, create_engine, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Mapped, mapped_column

from atpro.application.ports.unit_of_work import UnitOfWork
from atpro.infrastructure.database.base import Base
from atpro.infrastructure.database.session import SessionFactory
from atpro.infrastructure.database.unit_of_work import SqlAlchemyUnitOfWork
from atpro.infrastructure.database.unit_of_work_error import (
    UnitOfWorkAlreadyCommittedError,
    UnitOfWorkClosedError,
)


class _UowRow(Base):
    """Modele ORM minimal pour les tests UoW."""

    __tablename__ = "bl026_uow_rows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    label: Mapped[str] = mapped_column(String(32), nullable=False)


class TestSqlAlchemyUnitOfWork:
    def _engine(self) -> Engine:
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine, tables=[_UowRow.__table__])
        return engine

    def test_FEAT_016_2_port_est_abstrait(self) -> None:
        assert issubclass(SqlAlchemyUnitOfWork, UnitOfWork)

    def test_FEAT_016_2_commit_persiste(self) -> None:
        engine = self._engine()
        factory = SessionFactory(engine)
        try:
            with SqlAlchemyUnitOfWork(factory) as uow:
                uow.session.add(_UowRow(label="ok"))
                uow.commit()

            with SqlAlchemyUnitOfWork(factory) as uow:
                labels = list(uow.session.scalars(select(_UowRow.label)))
                uow.commit()
            assert labels == ["ok"]
        finally:
            engine.dispose()

    def test_FEAT_016_2_exception_declenche_rollback(self) -> None:
        engine = self._engine()
        factory = SessionFactory(engine)
        try:
            with pytest.raises(RuntimeError, match="boom"):
                with SqlAlchemyUnitOfWork(factory) as uow:
                    uow.session.add(_UowRow(label="orphan"))
                    uow.session.flush()
                    raise RuntimeError("boom")

            with SqlAlchemyUnitOfWork(factory) as uow:
                rows = list(uow.session.scalars(select(_UowRow)))
                uow.commit()
            assert rows == []
        finally:
            engine.dispose()

    def test_FEAT_016_2_sans_commit_rollback_a_la_sortie(self) -> None:
        engine = self._engine()
        factory = SessionFactory(engine)
        try:
            with SqlAlchemyUnitOfWork(factory) as uow:
                uow.session.add(_UowRow(label="forgotten"))
                uow.session.flush()

            with SqlAlchemyUnitOfWork(factory) as uow:
                rows = list(uow.session.scalars(select(_UowRow)))
                uow.commit()
            assert rows == []
        finally:
            engine.dispose()

    def test_FEAT_016_2_fermeture_session(self) -> None:
        engine = self._engine()
        factory = SessionFactory(engine)
        try:
            uow = SqlAlchemyUnitOfWork(factory)
            with uow:
                assert uow.session is not None
            with pytest.raises(UnitOfWorkClosedError):
                _ = uow.session
        finally:
            engine.dispose()

    def test_FEAT_016_2_double_commit_refuse(self) -> None:
        engine = self._engine()
        factory = SessionFactory(engine)
        try:
            with SqlAlchemyUnitOfWork(factory) as uow:
                uow.session.add(_UowRow(label="once"))
                uow.commit()
                with pytest.raises(UnitOfWorkAlreadyCommittedError):
                    uow.commit()
        finally:
            engine.dispose()

    def test_FEAT_016_2_reutilisation_apres_fermeture(self) -> None:
        engine = self._engine()
        factory = SessionFactory(engine)
        try:
            uow = SqlAlchemyUnitOfWork(factory)
            with uow:
                uow.commit()
            with pytest.raises(UnitOfWorkClosedError):
                with uow:
                    pass
        finally:
            engine.dispose()

    def test_FEAT_016_2_double_entree_refusee(self) -> None:
        engine = self._engine()
        factory = SessionFactory(engine)
        try:
            uow = SqlAlchemyUnitOfWork(factory)
            uow.__enter__()
            with pytest.raises(UnitOfWorkClosedError, match="deja ouverte"):
                uow.__enter__()
            uow.rollback()
            uow.close()
        finally:
            engine.dispose()
