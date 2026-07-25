"""Modele AgentDailyActivity.

:spec: FEAT-005.1
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

from atpro.domain.exceptions.domain_error import DomainError
from atpro.domain.value_objects.duration_seconds import DurationSeconds
from atpro.domain.value_objects.percentage import Percentage


@dataclass(frozen=True, slots=True)
class AgentDailyActivity:
    """Activite journaliere normalisee d'un agent.

    :param id: Identifiant interne.
    :param agent_id: Agent rapproche (nullable).
    :param raw_agent_name: Nom agent brut.
    :param site_id: Site (nullable).
    :param activity_date: Jour d'activite.
    :param received_calls: Appels recus.
    :param answered_calls: Appels repondus.
    :param outgoing_calls: Appels sortants.
    :param transferred_in_calls: Transferts entrants.
    :param handled_calls_total: Total traites.
    :param transferred_calls: Transferts.
    :param hold_count: Nombre de mises en garde.
    :param consultation_count: Consultations.
    :param login_time_seconds: Temps login.
    :param ready_time_seconds: Temps pret.
    :param not_ready_time_seconds: Temps non pret.
    :param phone_time_seconds: Temps telephone.
    :param incoming_talk_time_seconds: Parole entrante.
    :param outgoing_talk_time_seconds: Parole sortante.
    :param after_call_work_seconds: Post-appel.
    :param rona_time_seconds: Temps RONA.
    :param hold_duration_seconds: Duree mise en garde.
    :param answer_rate: Taux de reponse (ratio).
    :param hold_rate: Taux de mise en garde (ratio).
    :param raw_metrics: Metriques brutes residuelles.
    :param source_import_batch_id: Lot d'import (provenance).
    :param line_fingerprint: Empreinte ligne (provenance).
    :param created_at: Creation.
    :spec: FEAT-005.1
    """

    id: str
    agent_id: str | None
    raw_agent_name: str
    site_id: str | None
    activity_date: date
    received_calls: int
    answered_calls: int
    outgoing_calls: int
    transferred_in_calls: int
    handled_calls_total: int
    transferred_calls: int
    hold_count: int
    consultation_count: int
    login_time_seconds: DurationSeconds
    ready_time_seconds: DurationSeconds
    not_ready_time_seconds: DurationSeconds
    phone_time_seconds: DurationSeconds
    incoming_talk_time_seconds: DurationSeconds
    outgoing_talk_time_seconds: DurationSeconds
    after_call_work_seconds: DurationSeconds
    rona_time_seconds: DurationSeconds
    hold_duration_seconds: DurationSeconds
    answer_rate: Percentage | None
    hold_rate: Percentage | None
    raw_metrics: dict[str, Any] | None
    source_import_batch_id: str | None
    line_fingerprint: str | None
    created_at: datetime

    def __post_init__(self) -> None:
        """Valide les champs obligatoires.

        :raises DomainError: Si un champ est invalide.
        """
        if not self.id.strip():
            raise DomainError("AgentDailyActivity.id obligatoire")
        if not self.raw_agent_name.strip():
            raise DomainError("AgentDailyActivity.raw_agent_name obligatoire")
        for name, value in (
            ("received_calls", self.received_calls),
            ("answered_calls", self.answered_calls),
            ("outgoing_calls", self.outgoing_calls),
            ("transferred_in_calls", self.transferred_in_calls),
            ("handled_calls_total", self.handled_calls_total),
            ("transferred_calls", self.transferred_calls),
            ("hold_count", self.hold_count),
            ("consultation_count", self.consultation_count),
        ):
            if value < 0:
                raise DomainError(f"AgentDailyActivity.{name} negatif")
