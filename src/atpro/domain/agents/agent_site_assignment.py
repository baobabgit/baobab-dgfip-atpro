"""Modele AgentSiteAssignment.

:spec: FEAT-005.1
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from atpro.domain.exceptions.domain_error import DomainError


@dataclass(frozen=True, slots=True)
class AgentSiteAssignment:
    """Rattachement date d'un agent a un site.

    :param id: Identifiant interne.
    :param agent_id: Agent concerne.
    :param site_id: Site de rattachement.
    :param start_date: Debut de validite.
    :param end_date: Fin de validite (nullable).
    :param source: Provenance du rattachement.
    :param created_at: Horodatage de creation.
    :spec: FEAT-005.1
    """

    id: str
    agent_id: str
    site_id: str
    start_date: date
    end_date: date | None
    source: str
    created_at: datetime

    def __post_init__(self) -> None:
        """Valide les champs obligatoires et la coherence des dates.

        :raises DomainError: Si la plage est invalide.
        """
        if not self.id.strip():
            raise DomainError("AgentSiteAssignment.id obligatoire")
        if not self.agent_id.strip():
            raise DomainError("AgentSiteAssignment.agent_id obligatoire")
        if not self.site_id.strip():
            raise DomainError("AgentSiteAssignment.site_id obligatoire")
        if self.end_date is not None and self.start_date > self.end_date:
            raise DomainError("AgentSiteAssignment: start_date > end_date")
