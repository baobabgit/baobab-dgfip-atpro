"""Tests des modeles agents."""

from __future__ import annotations

from datetime import UTC, date, datetime

import pytest

from atpro.domain.agents import Agent, AgentAlias, AgentSiteAssignment
from atpro.domain.exceptions import DomainError


class TestAgent:
    """Instanciation Agent."""

    def test_FEAT_005_1_instantiate_agent(self) -> None:
        now = datetime(2026, 1, 1, tzinfo=UTC)
        agent = Agent(
            id="a1",
            first_name="Pascale",
            last_name="Maziere",
            display_name="Pascale Maziere",
            normalized_identity="maziere pascale",
            active=True,
            created_at=now,
            updated_at=now,
        )
        assert agent.display_name.startswith("Pascale")

    def test_FEAT_005_1_agent_requires_identity(self) -> None:
        now = datetime(2026, 1, 1, tzinfo=UTC)
        with pytest.raises(DomainError):
            Agent(
                id="a1",
                first_name="Pascale",
                last_name="Maziere",
                display_name=" ",
                normalized_identity="x",
                active=True,
                created_at=now,
                updated_at=now,
            )
        with pytest.raises(DomainError):
            Agent(
                id=" ",
                first_name="Pascale",
                last_name="Maziere",
                display_name="Pascale",
                normalized_identity="x",
                active=True,
                created_at=now,
                updated_at=now,
            )
        with pytest.raises(DomainError):
            Agent(
                id="a1",
                first_name="Pascale",
                last_name="Maziere",
                display_name="Pascale",
                normalized_identity=" ",
                active=True,
                created_at=now,
                updated_at=now,
            )


class TestAgentAlias:
    """Instanciation AgentAlias."""

    def test_FEAT_005_1_instantiate_alias(self) -> None:
        now = datetime(2026, 1, 1, tzinfo=UTC)
        alias = AgentAlias(
            id="al1",
            agent_id="a1",
            raw_alias="MAZIERE Pascale",
            normalized_alias="maziere pascale",
            source="incoming_calls",
            confidence=0.9,
            validated_by_user=False,
            created_at=now,
        )
        assert alias.confidence == 0.9

    def test_FEAT_005_1_alias_confidence_bounds(self) -> None:
        now = datetime(2026, 1, 1, tzinfo=UTC)
        with pytest.raises(DomainError):
            AgentAlias(
                id="al1",
                agent_id="a1",
                raw_alias="x",
                normalized_alias="x",
                source="s",
                confidence=1.5,
                validated_by_user=False,
                created_at=now,
            )
        with pytest.raises(DomainError):
            AgentAlias(
                id=" ",
                agent_id="a1",
                raw_alias="x",
                normalized_alias="x",
                source="s",
                confidence=0.5,
                validated_by_user=False,
                created_at=now,
            )
        with pytest.raises(DomainError):
            AgentAlias(
                id="al1",
                agent_id=" ",
                raw_alias="x",
                normalized_alias="x",
                source="s",
                confidence=0.5,
                validated_by_user=False,
                created_at=now,
            )
        with pytest.raises(DomainError):
            AgentAlias(
                id="al1",
                agent_id="a1",
                raw_alias=" ",
                normalized_alias="x",
                source="s",
                confidence=0.5,
                validated_by_user=False,
                created_at=now,
            )


class TestAgentSiteAssignment:
    """Instanciation AgentSiteAssignment."""

    def test_FEAT_005_1_instantiate_assignment(self) -> None:
        now = datetime(2026, 1, 1, tzinfo=UTC)
        assignment = AgentSiteAssignment(
            id="as1",
            agent_id="a1",
            site_id="s1",
            start_date=date(2026, 1, 1),
            end_date=None,
            source="manual",
            created_at=now,
        )
        assert assignment.end_date is None

    def test_FEAT_005_1_assignment_invalid_dates(self) -> None:
        now = datetime(2026, 1, 1, tzinfo=UTC)
        with pytest.raises(DomainError):
            AgentSiteAssignment(
                id="as1",
                agent_id="a1",
                site_id="s1",
                start_date=date(2026, 2, 1),
                end_date=date(2026, 1, 1),
                source="manual",
                created_at=now,
            )
        with pytest.raises(DomainError):
            AgentSiteAssignment(
                id=" ",
                agent_id="a1",
                site_id="s1",
                start_date=date(2026, 1, 1),
                end_date=None,
                source="manual",
                created_at=now,
            )
        with pytest.raises(DomainError):
            AgentSiteAssignment(
                id="as1",
                agent_id=" ",
                site_id="s1",
                start_date=date(2026, 1, 1),
                end_date=None,
                source="manual",
                created_at=now,
            )
        with pytest.raises(DomainError):
            AgentSiteAssignment(
                id="as1",
                agent_id="a1",
                site_id=" ",
                start_date=date(2026, 1, 1),
                end_date=None,
                source="manual",
                created_at=now,
            )
