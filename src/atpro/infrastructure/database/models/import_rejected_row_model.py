"""Modele ORM d'une ligne rejetee d'import.

:spec: FEAT-019.1
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from atpro.infrastructure.database.base import Base


class ImportRejectedRowModel(Base):
    """Table ``import_rejected_rows`` — quarantaine de lignes.

    :spec: FEAT-019.1
    """

    __tablename__ = "import_rejected_rows"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    import_batch_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("import_batches.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    row_number: Mapped[int] = mapped_column(Integer, nullable=False)
    severity: Mapped[str] = mapped_column(String(32), nullable=False)
    error_code: Mapped[str] = mapped_column(String(64), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    masked_payload: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
