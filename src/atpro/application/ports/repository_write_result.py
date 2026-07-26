"""Resultat explicite d'une ecriture repository.

:spec: FEAT-018.1
"""

from __future__ import annotations

from dataclasses import dataclass

from atpro.application.ports.repository_write_outcome import RepositoryWriteOutcome


@dataclass(frozen=True, slots=True)
class RepositoryWriteResult[T]:
    """Resultat d'ajout pour un agregat domaine.

    :param outcome: Created, existing ou conflict.
    :param entity: Entite persistee ou existante (jamais un ORM).
    :param message: Detail optionnel (conflit).
    :spec: FEAT-018.1
    """

    outcome: RepositoryWriteOutcome
    entity: T
    message: str | None = None
