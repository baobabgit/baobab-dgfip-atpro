"""Modele ORM Ticket.

:spec: FEAT-017.2
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from atpro.infrastructure.database.base import Base


class TicketModel(Base):
    """Table ``tickets`` — tickets metier.

    :spec: FEAT-017.2
    """

    __tablename__ = "tickets"
    __table_args__ = (
        UniqueConstraint(
            "source_system",
            "external_ticket_id",
            name="uq_tickets_source_external",
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    source_system: Mapped[str] = mapped_column(String(64), nullable=False)
    external_ticket_id: Mapped[str] = mapped_column(String(128), nullable=False)
    form_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    form_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    taken_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    closed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    channel: Mapped[str | None] = mapped_column(String(64), nullable=True)
    nature: Mapped[str | None] = mapped_column(String(128), nullable=True)
    ticket_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    status: Mapped[str | None] = mapped_column(String(64), nullable=True)
    contact_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    contact_identifier_hash: Mapped[str | None] = mapped_column(
        String(64), nullable=True
    )
    creation_domain: Mapped[str | None] = mapped_column(String(128), nullable=True)
    distribution_site_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("sites.id", ondelete="SET NULL"),
        nullable=True,
    )
    resolution_group_level: Mapped[str | None] = mapped_column(
        String(64), nullable=True
    )
    business_domain: Mapped[str | None] = mapped_column(String(128), nullable=True)
    owner_agent_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("agents.id", ondelete="SET NULL"),
        nullable=True,
    )
    qualification_agent_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("agents.id", ondelete="SET NULL"),
        nullable=True,
    )
    qualification_site_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("sites.id", ondelete="SET NULL"),
        nullable=True,
    )
    resolution_agent_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("agents.id", ondelete="SET NULL"),
        nullable=True,
    )
    resolution_site_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("sites.id", ondelete="SET NULL"),
        nullable=True,
    )
    closure_agent_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("agents.id", ondelete="SET NULL"),
        nullable=True,
    )
    source_import_batch_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("import_batches.id", ondelete="SET NULL"),
        nullable=True,
    )
    line_fingerprint: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at_db: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    updated_at_db: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
