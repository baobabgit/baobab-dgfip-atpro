"""Tables imports et referentiels v0.2.0.

Revision ID: 20260726_imports_referentiels
Revises: 20260726_baseline
Create Date: 2026-07-26

:spec: FEAT-017.2
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260726_imports_referentiels"
down_revision: str | None = "20260726_baseline"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Cree import_batches, referentiels et import_rejected_rows."""
    op.create_table(
        "import_batches",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("original_filename", sa.String(length=512), nullable=False),
        sa.Column("stored_filename", sa.String(length=512), nullable=True),
        sa.Column("sha256", sa.String(length=64), nullable=False),
        sa.Column("detected_type", sa.String(length=64), nullable=True),
        sa.Column("schema_version", sa.String(length=64), nullable=True),
        sa.Column("period_start", sa.Date(), nullable=True),
        sa.Column("period_end", sa.Date(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by", sa.String(length=128), nullable=True),
        sa.Column("accepted_rows", sa.Integer(), nullable=False),
        sa.Column("rejected_rows", sa.Integer(), nullable=False),
        sa.Column("ignored_rows", sa.Integer(), nullable=False),
        sa.Column("inserted_records", sa.Integer(), nullable=False),
        sa.Column("updated_records", sa.Integer(), nullable=False),
        sa.Column("skipped_records", sa.Integer(), nullable=False),
        sa.Column("error_summary", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_import_batches")),
        sa.UniqueConstraint("sha256", name="uq_import_batches_sha256"),
    )

    op.create_table(
        "sites",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=256), nullable=False),
        sa.Column("normalized_name", sa.String(length=256), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source_import_batch_id", sa.String(length=36), nullable=True),
        sa.Column("line_fingerprint", sa.String(length=64), nullable=True),
        sa.ForeignKeyConstraint(
            ["source_import_batch_id"],
            ["import_batches.id"],
            name=op.f("fk_sites_source_import_batch_id_import_batches"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_sites")),
        sa.UniqueConstraint("code", name="uq_sites_code"),
        sa.UniqueConstraint("normalized_name", name="uq_sites_normalized_name"),
    )

    op.create_table(
        "agents",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("first_name", sa.String(length=128), nullable=False),
        sa.Column("last_name", sa.String(length=128), nullable=False),
        sa.Column("display_name", sa.String(length=256), nullable=False),
        sa.Column("normalized_identity", sa.String(length=256), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source_import_batch_id", sa.String(length=36), nullable=True),
        sa.Column("line_fingerprint", sa.String(length=64), nullable=True),
        sa.ForeignKeyConstraint(
            ["source_import_batch_id"],
            ["import_batches.id"],
            name=op.f("fk_agents_source_import_batch_id_import_batches"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_agents")),
        sa.UniqueConstraint(
            "normalized_identity",
            name="uq_agents_normalized_identity",
        ),
    )

    op.create_table(
        "agent_aliases",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("agent_id", sa.String(length=36), nullable=False),
        sa.Column("raw_alias", sa.String(length=256), nullable=False),
        sa.Column("normalized_alias", sa.String(length=256), nullable=False),
        sa.Column("source", sa.String(length=64), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("validated_by_user", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["agent_id"],
            ["agents.id"],
            name=op.f("fk_agent_aliases_agent_id_agents"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_agent_aliases")),
        sa.UniqueConstraint(
            "normalized_alias",
            name="uq_agent_aliases_normalized_alias",
        ),
    )
    op.create_index(
        op.f("ix_agent_aliases_agent_id"),
        "agent_aliases",
        ["agent_id"],
        unique=False,
    )

    op.create_table(
        "agent_site_assignments",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("agent_id", sa.String(length=36), nullable=False),
        sa.Column("site_id", sa.String(length=36), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("source", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["agent_id"],
            ["agents.id"],
            name=op.f("fk_agent_site_assignments_agent_id_agents"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["site_id"],
            ["sites.id"],
            name=op.f("fk_agent_site_assignments_site_id_sites"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_agent_site_assignments")),
        sa.UniqueConstraint(
            "agent_id",
            "site_id",
            "start_date",
            name="uq_agent_site_assignments_agent_site_start",
        ),
    )
    op.create_index(
        op.f("ix_agent_site_assignments_agent_id"),
        "agent_site_assignments",
        ["agent_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_agent_site_assignments_site_id"),
        "agent_site_assignments",
        ["site_id"],
        unique=False,
    )

    op.create_table(
        "import_rejected_rows",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("import_batch_id", sa.String(length=36), nullable=False),
        sa.Column("row_number", sa.Integer(), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False),
        sa.Column("error_code", sa.String(length=64), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("masked_payload", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["import_batch_id"],
            ["import_batches.id"],
            name=op.f("fk_import_rejected_rows_import_batch_id_import_batches"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_import_rejected_rows")),
    )
    op.create_index(
        op.f("ix_import_rejected_rows_import_batch_id"),
        "import_rejected_rows",
        ["import_batch_id"],
        unique=False,
    )


def downgrade() -> None:
    """Supprime les tables imports et referentiels."""
    op.drop_index(
        op.f("ix_import_rejected_rows_import_batch_id"),
        table_name="import_rejected_rows",
    )
    op.drop_table("import_rejected_rows")
    op.drop_index(
        op.f("ix_agent_site_assignments_site_id"),
        table_name="agent_site_assignments",
    )
    op.drop_index(
        op.f("ix_agent_site_assignments_agent_id"),
        table_name="agent_site_assignments",
    )
    op.drop_table("agent_site_assignments")
    op.drop_index(op.f("ix_agent_aliases_agent_id"), table_name="agent_aliases")
    op.drop_table("agent_aliases")
    op.drop_table("agents")
    op.drop_table("sites")
    op.drop_table("import_batches")
