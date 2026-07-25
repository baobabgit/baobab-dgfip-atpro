"""Ligne brute d'appel (format long par mesure).

:spec: FEAT-005.4
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RawCallRow:
    """Representation interne d'une ligne CSV d'appel.

    :param row_number: Numero de ligne source (1-indexe donnees).
    :param external_call_id: Identifiant appel source.
    :param caller: Numero appelant brut.
    :param callee: Numero appele brut.
    :param agent_name: Nom agent brut.
    :param started_at_raw: Debut brut.
    :param ended_at_raw: Fin brute.
    :param flow: Flux.
    :param service: Service.
    :param measure_name: Nom de mesure.
    :param measure_value: Valeur de mesure.
    :param qualification_category: Categorie qualification.
    :param qualification_reason: Motif qualification.
    :param hangup_origin: Origine raccroche.
    :spec: FEAT-005.4
    """

    row_number: int
    external_call_id: str | None
    caller: str | None
    callee: str | None
    agent_name: str | None
    started_at_raw: str | None
    ended_at_raw: str | None
    flow: str | None
    service: str | None
    measure_name: str | None
    measure_value: str | None
    qualification_category: str | None = None
    qualification_reason: str | None = None
    hangup_origin: str | None = None
