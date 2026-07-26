"""Modele ORM CallSegment.

:spec: FEAT-017.2
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from atpro.infrastructure.database.base import Base


class CallSegmentModel(Base):
    """Table ``call_segments`` — segments d'appel.

    :spec: FEAT-017.2
    """

    __tablename__ = "call_segments"
    __table_args__ = (
        UniqueConstraint(
            "call_id",
            "segment_index",
            name="uq_call_segments_call_index",
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    call_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("calls.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    segment_index: Mapped[int] = mapped_column(Integer, nullable=False)
    agent_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("agents.id", ondelete="SET NULL"),
        nullable=True,
    )
    raw_agent_name: Mapped[str] = mapped_column(String(256), nullable=False)
    site_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("sites.id", ondelete="SET NULL"),
        nullable=True,
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    talk_duration_seconds: Mapped[int] = mapped_column(Integer, nullable=False)
    hold_duration_seconds: Mapped[int] = mapped_column(Integer, nullable=False)
    qualification_category: Mapped[str | None] = mapped_column(
        String(128), nullable=True
    )
    qualification_reason: Mapped[str | None] = mapped_column(String(256), nullable=True)
    hangup_origin: Mapped[str | None] = mapped_column(String(64), nullable=True)
    source_row_numbers: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    line_fingerprint: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
