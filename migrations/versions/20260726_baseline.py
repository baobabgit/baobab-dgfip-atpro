"""Baseline vide — point de depart des revisions v0.2.0.

Revision ID: 20260726_baseline
Revises:
Create Date: 2026-07-26

Les tables metier seront ajoutees par BL-028 / BL-029.

:spec: FEAT-017.1
"""

from __future__ import annotations

from collections.abc import Sequence

revision: str = "20260726_baseline"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Aucune table dans la baseline (schema livre par revisions suivantes)."""


def downgrade() -> None:
    """Aucune operation (baseline vide)."""
