"""Modele CallSegment.

:spec: FEAT-005.1
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from atpro.domain.exceptions.domain_error import DomainError
from atpro.domain.value_objects.duration_seconds import DurationSeconds


@dataclass(frozen=True, slots=True)
class CallSegment:
    """Segment de presentation ou participation agent.

    :param id: Identifiant interne.
    :param call_id: Appel parent.
    :param segment_index: Index du segment.
    :param agent_id: Agent rapproche (nullable).
    :param raw_agent_name: Nom agent brut.
    :param site_id: Site (nullable).
    :param started_at: Debut.
    :param ended_at: Fin (nullable).
    :param talk_duration_seconds: Duree de parole.
    :param hold_duration_seconds: Duree de mise en garde.
    :param qualification_category: Categorie qualification.
    :param qualification_reason: Motif qualification.
    :param hangup_origin: Origine de raccrochage.
    :param source_row_numbers: Numeros de lignes source (provenance).
    :param line_fingerprint: Empreinte ligne (provenance).
    :param created_at: Creation.
    :spec: FEAT-005.1
    """

    id: str
    call_id: str
    segment_index: int
    agent_id: str | None
    raw_agent_name: str
    site_id: str | None
    started_at: datetime
    ended_at: datetime | None
    talk_duration_seconds: DurationSeconds
    hold_duration_seconds: DurationSeconds
    qualification_category: str | None
    qualification_reason: str | None
    hangup_origin: str | None
    source_row_numbers: tuple[int, ...]
    line_fingerprint: str | None
    created_at: datetime

    def __post_init__(self) -> None:
        """Valide les champs obligatoires.

        :raises DomainError: Si un champ est invalide.
        """
        if not self.id.strip():
            raise DomainError("CallSegment.id obligatoire")
        if not self.call_id.strip():
            raise DomainError("CallSegment.call_id obligatoire")
        if self.segment_index < 0:
            raise DomainError("CallSegment.segment_index negatif")
