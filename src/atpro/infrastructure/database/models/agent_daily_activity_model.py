"""Modele ORM AgentDailyActivity.

:spec: FEAT-017.2
"""

from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import (
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from atpro.infrastructure.database.base import Base


class AgentDailyActivityModel(Base):
    """Table ``agent_daily_activities`` — activites journalieres.

    :spec: FEAT-017.2
    """

    __tablename__ = "agent_daily_activities"
    __table_args__ = (
        UniqueConstraint(
            "raw_agent_name",
            "activity_date",
            "line_fingerprint",
            name="uq_agent_daily_activities_raw_date_fp",
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
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
    activity_date: Mapped[date] = mapped_column(Date, nullable=False)
    received_calls: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    answered_calls: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    outgoing_calls: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    transferred_in_calls: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    handled_calls_total: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    transferred_calls: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    hold_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    consultation_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    login_time_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    ready_time_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    not_ready_time_seconds: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    phone_time_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    incoming_talk_time_seconds: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    outgoing_talk_time_seconds: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    after_call_work_seconds: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    rona_time_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    hold_duration_seconds: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    answer_rate: Mapped[float | None] = mapped_column(Float, nullable=True)
    hold_rate: Mapped[float | None] = mapped_column(Float, nullable=True)
    raw_metrics: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_import_batch_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("import_batches.id", ondelete="SET NULL"),
        nullable=True,
    )
    line_fingerprint: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
