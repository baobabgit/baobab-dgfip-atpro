"""Modele Ticket.

:spec: FEAT-005.1
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from atpro.domain.exceptions.domain_error import DomainError


@dataclass(frozen=True, slots=True)
class Ticket:
    """Ticket metier.

    :param id: Identifiant interne.
    :param source_system: Systeme source.
    :param external_ticket_id: Identifiant externe.
    :param form_id: Identifiant formulaire.
    :param form_type: Type formulaire.
    :param created_at: Creation metier.
    :param taken_at: Prise en charge.
    :param resolved_at: Resolution.
    :param closed_at: Cloture.
    :param channel: Canal.
    :param nature: Nature.
    :param ticket_type: Type ticket.
    :param status: Statut.
    :param contact_type: Type contact.
    :param contact_identifier_hash: Empreinte contact (sensible hashee).
    :param creation_domain: Domaine creation.
    :param distribution_site_id: Site repartition.
    :param resolution_group_level: Niveau groupe resolution.
    :param business_domain: Domaine metier.
    :param owner_agent_id: Agent proprietaire.
    :param qualification_agent_id: Agent qualification.
    :param qualification_site_id: Site qualification.
    :param resolution_agent_id: Agent resolution.
    :param resolution_site_id: Site resolution.
    :param closure_agent_id: Agent cloture.
    :param source_import_batch_id: Lot d'import (provenance).
    :param line_fingerprint: Empreinte ligne (provenance).
    :param created_at_db: Creation en base logique.
    :param updated_at_db: Mise a jour en base logique.
    :spec: FEAT-005.1
    """

    id: str
    source_system: str
    external_ticket_id: str
    form_id: str | None
    form_type: str | None
    created_at: datetime
    taken_at: datetime | None
    resolved_at: datetime | None
    closed_at: datetime | None
    channel: str | None
    nature: str | None
    ticket_type: str | None
    status: str | None
    contact_type: str | None
    contact_identifier_hash: str | None
    creation_domain: str | None
    distribution_site_id: str | None
    resolution_group_level: str | None
    business_domain: str | None
    owner_agent_id: str | None
    qualification_agent_id: str | None
    qualification_site_id: str | None
    resolution_agent_id: str | None
    resolution_site_id: str | None
    closure_agent_id: str | None
    source_import_batch_id: str | None
    line_fingerprint: str | None
    created_at_db: datetime
    updated_at_db: datetime

    def __post_init__(self) -> None:
        """Valide les champs obligatoires.

        :raises DomainError: Si un champ obligatoire est vide.
        """
        if not self.id.strip():
            raise DomainError("Ticket.id obligatoire")
        if not self.external_ticket_id.strip():
            raise DomainError("Ticket.external_ticket_id obligatoire")
        if not self.source_system.strip():
            raise DomainError("Ticket.source_system obligatoire")
