"""Repository SQLAlchemy pour les agents.

:spec: FEAT-018.1
"""

from __future__ import annotations

from dataclasses import replace

from sqlalchemy import select
from sqlalchemy.orm import Session

from atpro.application.ports.agent_repository import AgentRepository
from atpro.application.ports.repository_write_outcome import RepositoryWriteOutcome
from atpro.application.ports.repository_write_result import RepositoryWriteResult
from atpro.domain.agents.agent import Agent
from atpro.infrastructure.database.mappers.agent_mapper import AgentMapper
from atpro.infrastructure.database.models.agent_model import AgentModel
from atpro.parser.normalizers.agent_name_normalizer import AgentNameNormalizer


class SqlAlchemyAgentRepository(AgentRepository):
    """Implementation SQLAlchemy de :class:`AgentRepository`.

    :spec: FEAT-018.1
    """

    def __init__(
        self,
        session: Session,
        *,
        mapper: AgentMapper | None = None,
        name_normalizer: AgentNameNormalizer | None = None,
    ) -> None:
        """Injecte session et collaborateurs.

        :param session: Session SQLAlchemy active.
        :param mapper: Mapper domaine/ORM.
        :param name_normalizer: Normaliseur de noms d'agents.
        """
        self._session = session
        self._mapper = mapper or AgentMapper()
        self._name_normalizer = name_normalizer or AgentNameNormalizer()

    def add(self, agent: Agent) -> RepositoryWriteResult[Agent]:
        """Cree ou reconcilie un agent.

        :param agent: Agent domaine.
        :returns: Resultat explicite.
        """
        identity = self._name_normalizer.normalize(agent.display_name)
        candidate = replace(
            agent,
            normalized_identity=identity.normalized_value,
            first_name=identity.first_name_hint or agent.first_name,
            last_name=identity.last_name_hint or agent.last_name,
        )

        existing = self.get_by_id(candidate.id) or self.get_by_normalized_identity(
            candidate.normalized_identity
        )
        if existing is not None:
            if self._is_same_content(existing, candidate):
                return RepositoryWriteResult(
                    outcome=RepositoryWriteOutcome.EXISTING,
                    entity=existing,
                )
            return RepositoryWriteResult(
                outcome=RepositoryWriteOutcome.CONFLICT,
                entity=existing,
                message=(
                    "Conflit de cle metier agent "
                    f"(normalized_identity={candidate.normalized_identity!r})."
                ),
            )

        self._session.add(self._mapper.to_model(candidate))
        self._session.flush()
        return RepositoryWriteResult(
            outcome=RepositoryWriteOutcome.CREATED,
            entity=candidate,
        )

    def get_by_id(self, agent_id: str) -> Agent | None:
        """Recherche par identifiant.

        :param agent_id: Identifiant.
        :returns: Agent ou ``None``.
        """
        row = self._session.get(AgentModel, agent_id)
        return self._mapper.to_domain(row) if row is not None else None

    def get_by_normalized_identity(self, normalized_identity: str) -> Agent | None:
        """Recherche par identite canonique.

        :param normalized_identity: Identite normalisee.
        :returns: Agent ou ``None``.
        """
        statement = select(AgentModel).where(
            AgentModel.normalized_identity == normalized_identity
        )
        row = self._session.scalars(statement).first()
        return self._mapper.to_domain(row) if row is not None else None

    def list(self, *, limit: int = 100, offset: int = 0) -> list[Agent]:
        """Liste bornee.

        :param limit: Nombre max.
        :param offset: Decalage.
        :returns: Agents.
        """
        statement = (
            select(AgentModel)
            .order_by(AgentModel.display_name)
            .offset(offset)
            .limit(limit)
        )
        return [self._mapper.to_domain(row) for row in self._session.scalars(statement)]

    @staticmethod
    def _is_same_content(existing: Agent, candidate: Agent) -> bool:
        """Compare le contenu metier (hors timestamps / provenance).

        :param existing: Agent en base.
        :param candidate: Agent candidat.
        :returns: ``True`` si contenu equivalent.
        """
        return (
            existing.display_name == candidate.display_name
            and existing.normalized_identity == candidate.normalized_identity
            and existing.first_name == candidate.first_name
            and existing.last_name == candidate.last_name
            and existing.active == candidate.active
        )
