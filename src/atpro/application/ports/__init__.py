"""Ports applicatifs (interfaces sans dependance infrastructure).

:spec: FEAT-016.2
"""

from __future__ import annotations

from atpro.application.ports.agent_repository import AgentRepository
from atpro.application.ports.repository_write_outcome import RepositoryWriteOutcome
from atpro.application.ports.repository_write_result import RepositoryWriteResult
from atpro.application.ports.site_repository import SiteRepository
from atpro.application.ports.unit_of_work import UnitOfWork

__all__: list[str] = [
    "AgentRepository",
    "RepositoryWriteOutcome",
    "RepositoryWriteResult",
    "SiteRepository",
    "UnitOfWork",
]
