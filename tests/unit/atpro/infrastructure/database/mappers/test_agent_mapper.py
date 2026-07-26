"""Tests unitaires de ``AgentMapper``.

:spec: FEAT-018.1
"""

from __future__ import annotations

from datetime import UTC, datetime

from atpro.domain.agents.agent import Agent
from atpro.infrastructure.database.mappers.agent_mapper import AgentMapper
from atpro.infrastructure.database.models.agent_model import AgentModel


class TestAgentMapper:
    def test_FEAT_018_1_roundtrip_agent(self) -> None:
        now = datetime(2026, 1, 1, tzinfo=UTC)
        agent = Agent(
            id="a1",
            first_name="Alice",
            last_name="Dupont",
            display_name="Alice Dupont",
            normalized_identity="alice dupont",
            active=True,
            created_at=now,
            updated_at=now,
            source_import_batch_id=None,
            line_fingerprint="fp",
        )
        mapper = AgentMapper()
        row = mapper.to_model(agent)
        assert isinstance(row, AgentModel)
        restored = mapper.to_domain(row)
        assert restored == agent
