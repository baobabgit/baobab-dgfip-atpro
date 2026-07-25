"""Ligne ticket brute apres mapping colonnes.

:spec: FEAT-007.1
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RawTicketRow:
    """Cellules tickets mappees, encore brutes.

    :param row_number: Numero de ligne CSV (1 = en-tete).
    :param external_ticket_id: Numero ticket.
    :param created_at_raw: Creation.
    :param taken_at_raw: Prise en charge.
    :param resolved_at_raw: Resolution.
    :param closed_at_raw: Cloture.
    :param channel: Canal.
    :param nature: Nature.
    :param ticket_type: Type.
    :param status: Statut.
    :param distribution_site: Site repartition.
    :param qualification_agent: Agent qualification.
    :param qualification_site: Site qualification.
    :param resolution_agent: Agent resolution.
    :param resolution_site: Site resolution.
    :param closure_agent: Agent cloture.
    :param group: Groupe.
    :param domain: Domaine.
    :param contact_type: Type contact.
    :param contact_identifier: Contact brut (a hasher).
    :param form_id: Formulaire.
    :param form_type: Type formulaire.
    :spec: FEAT-007.1
    """

    row_number: int
    external_ticket_id: str | None
    created_at_raw: str | None
    taken_at_raw: str | None
    resolved_at_raw: str | None
    closed_at_raw: str | None
    channel: str | None
    nature: str | None
    ticket_type: str | None
    status: str | None
    distribution_site: str | None
    qualification_agent: str | None
    qualification_site: str | None
    resolution_agent: str | None
    resolution_site: str | None
    closure_agent: str | None
    group: str | None
    domain: str | None
    contact_type: str | None
    contact_identifier: str | None
    form_id: str | None
    form_type: str | None
