"""Tests unitaires de ``SqlAlchemyAgentRepository``.

:spec: FEAT-018.1
"""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from atpro.application.ports.repository_write_outcome import RepositoryWriteOutcome
from atpro.domain.agents.agent import Agent
from atpro.infrastructure.database import models as _models
from atpro.infrastructure.database.base import Base
from atpro.infrastructure.database.repositories.agent_repository import (
    SqlAlchemyAgentRepository,
)
from atpro.infrastructure.database.session import SessionFactory


class TestSqlAlchemyAgentRepository:
    def _engine(self) -> Engine:
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(
            engine,
            tables=[
                _models.ImportBatchModel.__table__,
                _models.AgentModel.__table__,
            ],
        )
        return engine

    def _agent(
        self,
        *,
        agent_id: str = "agent-1",
        display_name: str = "Alice Dupont",
        first_name: str = "Alice",
        last_name: str = "Dupont",
        normalized_identity: str = "alice dupont",
        active: bool = True,
    ) -> Agent:
        now = datetime(2026, 1, 1, tzinfo=UTC)
        return Agent(
            id=agent_id,
            first_name=first_name,
            last_name=last_name,
            display_name=display_name,
            normalized_identity=normalized_identity,
            active=active,
            created_at=now,
            updated_at=now,
        )

    def test_FEAT_018_1_creation_agent(self) -> None:
        engine = self._engine()
        factory = SessionFactory(engine)
        try:
            session = factory.create_session()
            repo = SqlAlchemyAgentRepository(session)
            result = repo.add(self._agent())
            session.commit()
            assert result.outcome is RepositoryWriteOutcome.CREATED
            assert repo.get_by_id("agent-1") is not None
            assert (
                repo.get_by_normalized_identity(result.entity.normalized_identity)
                is not None
            )
        finally:
            engine.dispose()

    def test_FEAT_018_1_reimport_identique_agent(self) -> None:
        engine = self._engine()
        factory = SessionFactory(engine)
        try:
            session = factory.create_session()
            repo = SqlAlchemyAgentRepository(session)
            first = repo.add(self._agent())
            session.commit()
            second = repo.add(self._agent(agent_id="agent-other"))
            session.commit()
            assert first.outcome is RepositoryWriteOutcome.CREATED
            assert second.outcome is RepositoryWriteOutcome.EXISTING
            assert second.entity.id == "agent-1"
            assert len(repo.list()) == 1
        finally:
            engine.dispose()

    def test_FEAT_018_1_conflit_cle_metier_agent(self) -> None:
        engine = self._engine()
        factory = SessionFactory(engine)
        try:
            session = factory.create_session()
            repo = SqlAlchemyAgentRepository(session)
            repo.add(self._agent(display_name="Alice Dupont"))
            session.commit()
            conflict = repo.add(
                self._agent(
                    agent_id="agent-2",
                    display_name="alice dupont",
                    first_name="alice",
                    last_name="dupont",
                )
            )
            assert conflict.outcome is RepositoryWriteOutcome.CONFLICT
            assert conflict.message is not None
        finally:
            engine.dispose()

    def test_FEAT_018_1_recherche_agent_par_id(self) -> None:
        engine = self._engine()
        factory = SessionFactory(engine)
        try:
            session = factory.create_session()
            repo = SqlAlchemyAgentRepository(session)
            repo.add(self._agent())
            session.commit()
            found = repo.get_by_id("agent-1")
            assert found is not None
            assert found.display_name == "Alice Dupont"
        finally:
            engine.dispose()

    def test_FEAT_018_1_liste_agents_inclut_inactifs(self) -> None:
        engine = self._engine()
        factory = SessionFactory(engine)
        try:
            session = factory.create_session()
            repo = SqlAlchemyAgentRepository(session)
            repo.add(self._agent(active=False))
            session.commit()
            agents = repo.list()
            assert len(agents) == 1
            assert agents[0].active is False
        finally:
            engine.dispose()
