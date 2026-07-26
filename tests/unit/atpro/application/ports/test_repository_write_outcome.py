"""Tests unitaires des ports repository write.

:spec: FEAT-018.1
"""

from __future__ import annotations

from atpro.application.ports.agent_repository import AgentRepository
from atpro.application.ports.repository_write_outcome import RepositoryWriteOutcome
from atpro.application.ports.repository_write_result import RepositoryWriteResult
from atpro.application.ports.site_repository import SiteRepository


class TestRepositoryWritePorts:
    def test_FEAT_018_1_outcome_values(self) -> None:
        assert RepositoryWriteOutcome.CREATED.value == "created"
        assert RepositoryWriteOutcome.EXISTING.value == "existing"
        assert RepositoryWriteOutcome.CONFLICT.value == "conflict"

    def test_FEAT_018_1_result_holds_entity(self) -> None:
        result = RepositoryWriteResult(
            outcome=RepositoryWriteOutcome.CREATED,
            entity="payload",
            message=None,
        )
        assert result.entity == "payload"

    def test_FEAT_018_1_ports_sont_abstraits(self) -> None:
        assert SiteRepository.__abstractmethods__
        assert AgentRepository.__abstractmethods__
