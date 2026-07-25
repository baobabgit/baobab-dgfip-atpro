"""Modele Call.

:spec: FEAT-005.1
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from atpro.domain.enums.call_direction import CallDirection
from atpro.domain.exceptions.domain_error import DomainError


@dataclass(frozen=True, slots=True)
class Call:
    """Appel telephonique global.

    :param id: Identifiant interne.
    :param source_system: Systeme source.
    :param external_call_id: Identifiant externe.
    :param direction: Sens de l'appel.
    :param started_at: Debut.
    :param ended_at: Fin (nullable).
    :param caller_hash: Empreinte appelant.
    :param callee_hash: Empreinte appele.
    :param flow: Flux metier.
    :param service: Service.
    :param global_result: Resultat global.
    :param source_import_batch_id: Lot d'import (provenance).
    :param created_at: Creation.
    :param updated_at: Mise a jour.
    :param line_fingerprint: Empreinte ligne (provenance).
    :spec: FEAT-005.1
    """

    id: str
    source_system: str
    external_call_id: str
    direction: CallDirection
    started_at: datetime
    ended_at: datetime | None
    caller_hash: str | None
    callee_hash: str | None
    flow: str | None
    service: str | None
    global_result: str | None
    source_import_batch_id: str | None
    created_at: datetime
    updated_at: datetime
    line_fingerprint: str | None = None

    def __post_init__(self) -> None:
        """Valide les champs obligatoires.

        :raises DomainError: Si un champ obligatoire est vide.
        """
        if not self.id.strip():
            raise DomainError("Call.id obligatoire")
        if not self.external_call_id.strip():
            raise DomainError("Call.external_call_id obligatoire")
        if not self.source_system.strip():
            raise DomainError("Call.source_system obligatoire")
