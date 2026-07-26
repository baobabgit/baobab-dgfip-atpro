"""Modele ORM Site.

:spec: FEAT-017.2
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from atpro.infrastructure.database.base import Base


class SiteModel(Base):
    """Table ``sites`` — referentiel sites.

    :spec: FEAT-017.2
    """

    __tablename__ = "sites"
    __table_args__ = (
        UniqueConstraint("code", name="uq_sites_code"),
        UniqueConstraint("normalized_name", name="uq_sites_normalized_name"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    normalized_name: Mapped[str] = mapped_column(String(256), nullable=False)
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
