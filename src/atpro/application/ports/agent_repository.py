"""Port repository Agent.

:spec: FEAT-018.1
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from atpro.application.ports.repository_write_result import RepositoryWriteResult
from atpro.domain.agents.agent import Agent


class AgentRepository(ABC):
    """Persistance et consultation des agents (sans objets ORM).

    :spec: FEAT-018.1
    """

    @abstractmethod
    def add(self, agent: Agent) -> RepositoryWriteResult[Agent]:
        """Cree ou reconcilie un agent de facon idempotente.

        :param agent: Agent domaine.
        :returns: Resultat explicite (created / existing / conflict).
        """

    @abstractmethod
    def get_by_id(self, agent_id: str) -> Agent | None:
        """Recherche par identifiant interne.

        :param agent_id: Identifiant.
        :returns: Agent ou ``None``.
        """

    @abstractmethod
    def get_by_normalized_identity(self, normalized_identity: str) -> Agent | None:
        """Recherche par identite canonique.

        :param normalized_identity: Identite normalisee.
        :returns: Agent ou ``None``.
        """

    @abstractmethod
    def list(self, *, limit: int = 100, offset: int = 0) -> list[Agent]:
        """Liste bornee (CLI), y compris agents inactifs.

        :param limit: Nombre max.
        :param offset: Decalage.
        :returns: Agents.
        """
