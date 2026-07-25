"""Modele AgentAlias.

:spec: FEAT-005.1
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from atpro.domain.exceptions.domain_error import DomainError


@dataclass(frozen=True, slots=True)
class AgentAlias:
    """Alias observe pour un agent.

    :param id: Identifiant interne.
    :param agent_id: Agent rattache.
    :param raw_alias: Alias brut source.
    :param normalized_alias: Alias normalise.
    :param source: Provenance de l'alias.
    :param confidence: Score de confiance dans ``[0, 1]``.
    :param validated_by_user: Validation humaine.
    :param created_at: Horodatage de creation.
    :spec: FEAT-005.1
    """

    id: str
    agent_id: str
    raw_alias: str
    normalized_alias: str
    source: str
    confidence: float
    validated_by_user: bool
    created_at: datetime

    def __post_init__(self) -> None:
        """Valide les champs obligatoires.

        :raises DomainError: Si un champ est invalide.
        """
        if not self.id.strip():
            raise DomainError("AgentAlias.id obligatoire")
        if not self.agent_id.strip():
            raise DomainError("AgentAlias.agent_id obligatoire")
        if not self.raw_alias.strip():
            raise DomainError("AgentAlias.raw_alias obligatoire")
        if not 0.0 <= self.confidence <= 1.0:
            raise DomainError("AgentAlias.confidence hors [0, 1]")
