"""Resultat d'une ecriture repository.

:spec: FEAT-018.1
"""

from __future__ import annotations

from enum import StrEnum


class RepositoryWriteOutcome(StrEnum):
    """Issue d'une tentative d'ecriture idempotente.

    :spec: FEAT-018.1
    """

    CREATED = "created"
    EXISTING = "existing"
    CONFLICT = "conflict"
