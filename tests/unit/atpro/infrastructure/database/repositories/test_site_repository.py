"""Tests unitaires de ``SqlAlchemySiteRepository``.

:spec: FEAT-018.1
"""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from atpro.application.ports.repository_write_outcome import RepositoryWriteOutcome
from atpro.domain.sites.site import Site
from atpro.infrastructure.database import models as _models
from atpro.infrastructure.database.base import Base
from atpro.infrastructure.database.repositories.site_repository import (
    SqlAlchemySiteRepository,
)
from atpro.infrastructure.database.session import SessionFactory


class TestSqlAlchemySiteRepository:
    def _engine(self) -> Engine:
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(
            engine,
            tables=[
                _models.ImportBatchModel.__table__,
                _models.SiteModel.__table__,
            ],
        )
        return engine

    def _site(
        self,
        *,
        site_id: str = "site-1",
        code: str = "PAR",
        name: str = "Paris",
        normalized_name: str = "paris",
        active: bool = True,
    ) -> Site:
        now = datetime(2026, 1, 1, tzinfo=UTC)
        return Site(
            id=site_id,
            code=code,
            name=name,
            normalized_name=normalized_name,
            active=active,
            created_at=now,
            updated_at=now,
        )

    def test_FEAT_018_1_creation_site(self) -> None:
        engine = self._engine()
        factory = SessionFactory(engine)
        try:
            session = factory.create_session()
            repo = SqlAlchemySiteRepository(session)
            result = repo.add(self._site())
            session.commit()
            assert result.outcome is RepositoryWriteOutcome.CREATED
            assert result.entity.normalized_name == "paris"
            assert repo.get_by_id("site-1") is not None
            assert repo.get_by_code("PAR") is not None
        finally:
            engine.dispose()

    def test_FEAT_018_1_reimport_identique_site(self) -> None:
        engine = self._engine()
        factory = SessionFactory(engine)
        try:
            session = factory.create_session()
            repo = SqlAlchemySiteRepository(session)
            first = repo.add(self._site())
            session.commit()
            second = repo.add(self._site(site_id="site-other"))
            session.commit()
            assert first.outcome is RepositoryWriteOutcome.CREATED
            assert second.outcome is RepositoryWriteOutcome.EXISTING
            assert second.entity.id == "site-1"
            assert len(repo.list()) == 1
        finally:
            engine.dispose()

    def test_FEAT_018_1_conflit_cle_metier_site(self) -> None:
        engine = self._engine()
        factory = SessionFactory(engine)
        try:
            session = factory.create_session()
            repo = SqlAlchemySiteRepository(session)
            repo.add(self._site(name="Paris", code="PAR"))
            session.commit()
            conflict = repo.add(
                self._site(
                    site_id="site-2",
                    code="PAR",
                    name="Lyon",
                    normalized_name="lyon",
                )
            )
            assert conflict.outcome is RepositoryWriteOutcome.CONFLICT
            assert conflict.message is not None
            assert "PAR" in conflict.message
        finally:
            engine.dispose()

    def test_FEAT_018_1_recherche_par_id_et_nom_canonique(self) -> None:
        engine = self._engine()
        factory = SessionFactory(engine)
        try:
            session = factory.create_session()
            repo = SqlAlchemySiteRepository(session)
            created = repo.add(self._site(name="Paris Centre"))
            session.commit()
            assert created.outcome is RepositoryWriteOutcome.CREATED
            by_id = repo.get_by_id("site-1")
            assert by_id is not None
            by_name = repo.get_by_normalized_name(by_id.normalized_name)
            assert by_name is not None
            assert by_name.id == "site-1"
        finally:
            engine.dispose()

    def test_FEAT_018_1_liste_inclut_inactifs(self) -> None:
        engine = self._engine()
        factory = SessionFactory(engine)
        try:
            session = factory.create_session()
            repo = SqlAlchemySiteRepository(session)
            repo.add(self._site(active=False))
            session.commit()
            sites = repo.list()
            assert len(sites) == 1
            assert sites[0].active is False
        finally:
            engine.dispose()
