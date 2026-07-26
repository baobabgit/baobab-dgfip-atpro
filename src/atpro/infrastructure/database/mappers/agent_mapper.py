"""Mapper Agent domaine ↔ ORM.

:spec: FEAT-018.1
"""

from __future__ import annotations

from atpro.domain.agents.agent import Agent
from atpro.infrastructure.database.models.agent_model import AgentModel


class AgentMapper:
    """Conversion bidirectionnelle Agent / AgentModel.

    :spec: FEAT-018.1
    """

    def to_domain(self, row: AgentModel) -> Agent:
        """ORM vers domaine.

        :param row: Ligne ORM.
        :returns: Agent domaine.
        """
        return Agent(
            id=row.id,
            first_name=row.first_name,
            last_name=row.last_name,
            display_name=row.display_name,
            normalized_identity=row.normalized_identity,
            active=row.active,
            created_at=row.created_at,
            updated_at=row.updated_at,
            source_import_batch_id=row.source_import_batch_id,
            line_fingerprint=row.line_fingerprint,
        )

    def to_model(self, agent: Agent) -> AgentModel:
        """Domaine vers ORM.

        :param agent: Agent domaine.
        :returns: Ligne ORM non attachee.
        """
        return AgentModel(
            id=agent.id,
            first_name=agent.first_name,
            last_name=agent.last_name,
            display_name=agent.display_name,
            normalized_identity=agent.normalized_identity,
            active=agent.active,
            created_at=agent.created_at,
            updated_at=agent.updated_at,
            source_import_batch_id=agent.source_import_batch_id,
            line_fingerprint=agent.line_fingerprint,
        )
