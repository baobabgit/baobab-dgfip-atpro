"""Modele ORM du lot d'import.

:spec: FEAT-019.1
"""

from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Date, DateTime, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from atpro.infrastructure.database.base import Base


class ImportBatchModel(Base):
    """Table ``import_batches`` — tracabilite d'un fichier importe.

    :spec: FEAT-019.1
    """

    __tablename__ = "import_batches"
    __table_args__ = (UniqueConstraint("sha256", name="uq_import_batches_sha256"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    original_filename: Mapped[str] = mapped_column(String(512), nullable=False)
    stored_filename: Mapped[str | None] = mapped_column(String(512), nullable=True)
    sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    detected_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    schema_version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    period_start: Mapped[date | None] = mapped_column(Date, nullable=True)
    period_end: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    accepted_rows: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rejected_rows: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    ignored_rows: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    inserted_records: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    updated_records: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    skipped_records: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    error_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
