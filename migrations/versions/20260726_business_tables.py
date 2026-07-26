"""Tables metier importees v0.2.0.

Revision ID: 20260726_business_tables
Revises: 20260726_imports_referentiels
Create Date: 2026-07-26

:spec: FEAT-017.2
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260726_business_tables"
down_revision: str | None = "20260726_imports_referentiels"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Cree calls, call_segments, tickets et agent_daily_activities."""
    op.create_table(
        "calls",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("source_system", sa.String(length=64), nullable=False),
        sa.Column("external_call_id", sa.String(length=128), nullable=False),
        sa.Column("direction", sa.String(length=16), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("caller_hash", sa.String(length=64), nullable=True),
        sa.Column("callee_hash", sa.String(length=64), nullable=True),
        sa.Column("flow", sa.String(length=128), nullable=True),
        sa.Column("service", sa.String(length=128), nullable=True),
        sa.Column("global_result", sa.String(length=128), nullable=True),
        sa.Column("source_import_batch_id", sa.String(length=36), nullable=True),
        sa.Column("line_fingerprint", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["source_import_batch_id"],
            ["import_batches.id"],
            name=op.f("fk_calls_source_import_batch_id_import_batches"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_calls")),
        sa.UniqueConstraint(
            "source_system",
            "external_call_id",
            name="uq_calls_source_external",
        ),
    )

    op.create_table(
        "call_segments",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("call_id", sa.String(length=36), nullable=False),
        sa.Column("segment_index", sa.Integer(), nullable=False),
        sa.Column("agent_id", sa.String(length=36), nullable=True),
        sa.Column("raw_agent_name", sa.String(length=256), nullable=False),
        sa.Column("site_id", sa.String(length=36), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("talk_duration_seconds", sa.Integer(), nullable=False),
        sa.Column("hold_duration_seconds", sa.Integer(), nullable=False),
        sa.Column("qualification_category", sa.String(length=128), nullable=True),
        sa.Column("qualification_reason", sa.String(length=256), nullable=True),
        sa.Column("hangup_origin", sa.String(length=64), nullable=True),
        sa.Column("source_row_numbers", sa.Text(), nullable=False),
        sa.Column("line_fingerprint", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["agent_id"],
            ["agents.id"],
            name=op.f("fk_call_segments_agent_id_agents"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["call_id"],
            ["calls.id"],
            name=op.f("fk_call_segments_call_id_calls"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["site_id"],
            ["sites.id"],
            name=op.f("fk_call_segments_site_id_sites"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_call_segments")),
        sa.UniqueConstraint(
            "call_id",
            "segment_index",
            name="uq_call_segments_call_index",
        ),
    )
    op.create_index(
        op.f("ix_call_segments_call_id"),
        "call_segments",
        ["call_id"],
        unique=False,
    )

    op.create_table(
        "tickets",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("source_system", sa.String(length=64), nullable=False),
        sa.Column("external_ticket_id", sa.String(length=128), nullable=False),
        sa.Column("form_id", sa.String(length=64), nullable=True),
        sa.Column("form_type", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("taken_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("channel", sa.String(length=64), nullable=True),
        sa.Column("nature", sa.String(length=128), nullable=True),
        sa.Column("ticket_type", sa.String(length=64), nullable=True),
        sa.Column("status", sa.String(length=64), nullable=True),
        sa.Column("contact_type", sa.String(length=64), nullable=True),
        sa.Column("contact_identifier_hash", sa.String(length=64), nullable=True),
        sa.Column("creation_domain", sa.String(length=128), nullable=True),
        sa.Column("distribution_site_id", sa.String(length=36), nullable=True),
        sa.Column("resolution_group_level", sa.String(length=64), nullable=True),
        sa.Column("business_domain", sa.String(length=128), nullable=True),
        sa.Column("owner_agent_id", sa.String(length=36), nullable=True),
        sa.Column("qualification_agent_id", sa.String(length=36), nullable=True),
        sa.Column("qualification_site_id", sa.String(length=36), nullable=True),
        sa.Column("resolution_agent_id", sa.String(length=36), nullable=True),
        sa.Column("resolution_site_id", sa.String(length=36), nullable=True),
        sa.Column("closure_agent_id", sa.String(length=36), nullable=True),
        sa.Column("source_import_batch_id", sa.String(length=36), nullable=True),
        sa.Column("line_fingerprint", sa.String(length=64), nullable=True),
        sa.Column("created_at_db", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at_db", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["closure_agent_id"],
            ["agents.id"],
            name=op.f("fk_tickets_closure_agent_id_agents"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["distribution_site_id"],
            ["sites.id"],
            name=op.f("fk_tickets_distribution_site_id_sites"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["owner_agent_id"],
            ["agents.id"],
            name=op.f("fk_tickets_owner_agent_id_agents"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["qualification_agent_id"],
            ["agents.id"],
            name=op.f("fk_tickets_qualification_agent_id_agents"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["qualification_site_id"],
            ["sites.id"],
            name=op.f("fk_tickets_qualification_site_id_sites"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["resolution_agent_id"],
            ["agents.id"],
            name=op.f("fk_tickets_resolution_agent_id_agents"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["resolution_site_id"],
            ["sites.id"],
            name=op.f("fk_tickets_resolution_site_id_sites"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["source_import_batch_id"],
            ["import_batches.id"],
            name=op.f("fk_tickets_source_import_batch_id_import_batches"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tickets")),
        sa.UniqueConstraint(
            "source_system",
            "external_ticket_id",
            name="uq_tickets_source_external",
        ),
    )

    op.create_table(
        "agent_daily_activities",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("agent_id", sa.String(length=36), nullable=True),
        sa.Column("raw_agent_name", sa.String(length=256), nullable=False),
        sa.Column("site_id", sa.String(length=36), nullable=True),
        sa.Column("activity_date", sa.Date(), nullable=False),
        sa.Column("received_calls", sa.Integer(), nullable=False),
        sa.Column("answered_calls", sa.Integer(), nullable=False),
        sa.Column("outgoing_calls", sa.Integer(), nullable=False),
        sa.Column("transferred_in_calls", sa.Integer(), nullable=False),
        sa.Column("handled_calls_total", sa.Integer(), nullable=False),
        sa.Column("transferred_calls", sa.Integer(), nullable=False),
        sa.Column("hold_count", sa.Integer(), nullable=False),
        sa.Column("consultation_count", sa.Integer(), nullable=False),
        sa.Column("login_time_seconds", sa.Integer(), nullable=False),
        sa.Column("ready_time_seconds", sa.Integer(), nullable=False),
        sa.Column("not_ready_time_seconds", sa.Integer(), nullable=False),
        sa.Column("phone_time_seconds", sa.Integer(), nullable=False),
        sa.Column("incoming_talk_time_seconds", sa.Integer(), nullable=False),
        sa.Column("outgoing_talk_time_seconds", sa.Integer(), nullable=False),
        sa.Column("after_call_work_seconds", sa.Integer(), nullable=False),
        sa.Column("rona_time_seconds", sa.Integer(), nullable=False),
        sa.Column("hold_duration_seconds", sa.Integer(), nullable=False),
        sa.Column("answer_rate", sa.Float(), nullable=True),
        sa.Column("hold_rate", sa.Float(), nullable=True),
        sa.Column("raw_metrics", sa.Text(), nullable=True),
        sa.Column("source_import_batch_id", sa.String(length=36), nullable=True),
        sa.Column("line_fingerprint", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["agent_id"],
            ["agents.id"],
            name=op.f("fk_agent_daily_activities_agent_id_agents"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["site_id"],
            ["sites.id"],
            name=op.f("fk_agent_daily_activities_site_id_sites"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["source_import_batch_id"],
            ["import_batches.id"],
            name=op.f(
                "fk_agent_daily_activities_source_import_batch_id_import_batches"
            ),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_agent_daily_activities")),
        sa.UniqueConstraint(
            "raw_agent_name",
            "activity_date",
            "line_fingerprint",
            name="uq_agent_daily_activities_raw_date_fp",
        ),
    )


def downgrade() -> None:
    """Supprime les tables metier."""
    op.drop_table("agent_daily_activities")
    op.drop_table("tickets")
    op.drop_index(op.f("ix_call_segments_call_id"), table_name="call_segments")
    op.drop_table("call_segments")
    op.drop_table("calls")
