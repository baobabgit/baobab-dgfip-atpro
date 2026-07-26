"""Modele ORM AgentAlias.

:spec: FEAT-017.2
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from atpro.infrastructure.database.base import Base


class AgentAliasModel(Base):
    """Table ``agent_aliases`` — variantes de noms agents.

    :spec: FEAT-017.2
    """

    __tablename__ = "agent_aliases"
    __table_args__ = (
        UniqueConstraint(
            "normalized_alias",
            name="uq_agent_aliases_normalized_alias",
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    agent_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("agents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    raw_alias: Mapped[str] = mapped_column(String(256), nullable=False)
    normalized_alias: Mapped[str] = mapped_column(String(256), nullable=False)
    source: Mapped[str] = mapped_column(String(64), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    validated_by_user: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
