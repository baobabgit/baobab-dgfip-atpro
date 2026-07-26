"""Modele ORM Call.

:spec: FEAT-017.2
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from atpro.infrastructure.database.base import Base


class CallModel(Base):
    """Table ``calls`` — appels consolides.

    :spec: FEAT-017.2
    """

    __tablename__ = "calls"
    __table_args__ = (
        UniqueConstraint(
            "source_system",
            "external_call_id",
            name="uq_calls_source_external",
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    source_system: Mapped[str] = mapped_column(String(64), nullable=False)
    external_call_id: Mapped[str] = mapped_column(String(128), nullable=False)
    direction: Mapped[str] = mapped_column(String(16), nullable=False)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    caller_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    callee_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    flow: Mapped[str | None] = mapped_column(String(128), nullable=True)
    service: Mapped[str | None] = mapped_column(String(128), nullable=True)
    global_result: Mapped[str | None] = mapped_column(String(128), nullable=True)
    source_import_batch_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("import_batches.id", ondelete="SET NULL"),
        nullable=True,
    )
    line_fingerprint: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
