"""Modele ORM Agent.

:spec: FEAT-017.2
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from atpro.infrastructure.database.base import Base


class AgentModel(Base):
    """Table ``agents`` — referentiel agents.

    :spec: FEAT-017.2
    """

    __tablename__ = "agents"
    __table_args__ = (
        UniqueConstraint(
            "normalized_identity",
            name="uq_agents_normalized_identity",
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    first_name: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    last_name: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    display_name: Mapped[str] = mapped_column(String(256), nullable=False)
    normalized_identity: Mapped[str] = mapped_column(String(256), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    source_import_batch_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("import_batches.id", ondelete="SET NULL"),
        nullable=True,
    )
    line_fingerprint: Mapped[str | None] = mapped_column(String(64), nullable=True)
