"""Modele ORM AgentSiteAssignment.

:spec: FEAT-017.2
"""

from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from atpro.infrastructure.database.base import Base


class AgentSiteAssignmentModel(Base):
    """Table ``agent_site_assignments`` — rattachements dates.

    :spec: FEAT-017.2
    """

    __tablename__ = "agent_site_assignments"
    __table_args__ = (
        UniqueConstraint(
            "agent_id",
            "site_id",
            "start_date",
            name="uq_agent_site_assignments_agent_site_start",
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    agent_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("agents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    site_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("sites.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    source: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
