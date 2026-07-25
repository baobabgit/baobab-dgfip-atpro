"""Catalogue des mesures d'activite agents reconnues.

:spec: FEAT-008.1
:spec: FEAT-009.1
"""

from __future__ import annotations

from typing import ClassVar


class KnownActivityMeasure:
    """Mappe une cle HeaderNormalizer vers un champ ``AgentDailyActivity``.

    La forme retournee est ``(field_name, kind)`` avec
    ``kind`` dans ``{"count", "duration", "percent"}``.

    :spec: FEAT-008.1
    :spec: FEAT-009.1
    """

    _MAP: ClassVar[dict[str, tuple[str, str]]] = {
        "appels_decroches": ("answered_calls", "count"),
        "appels_recus": ("received_calls", "count"),
        "nombre_d_appels_sortants": ("outgoing_calls", "count"),
        "appels_sortants": ("outgoing_calls", "count"),
        "transferts_entrants": ("transferred_in_calls", "count"),
        "appels_traites": ("handled_calls_total", "count"),
        "transferts": ("transferred_calls", "count"),
        "mises_en_garde": ("hold_count", "count"),
        "consultations": ("consultation_count", "count"),
        "temps_login": ("login_time_seconds", "duration"),
        "temps_pret": ("ready_time_seconds", "duration"),
        "temps_non_pret": ("not_ready_time_seconds", "duration"),
        "temps_telephone": ("phone_time_seconds", "duration"),
        "temps_communication_entrants": ("incoming_talk_time_seconds", "duration"),
        "temps_communication_sortants": ("outgoing_talk_time_seconds", "duration"),
        "temps_post_appel": ("after_call_work_seconds", "duration"),
        "temps_total_dans_l_etat_rona": ("rona_time_seconds", "duration"),
        "temps_total_dans_letat_rona": ("rona_time_seconds", "duration"),
        "duree_de_mise_en_garde": ("hold_duration_seconds", "duration"),
        "taux_de_decroches": ("answer_rate", "percent"),
        "taux_de_mise_en_garde": ("hold_rate", "percent"),
    }

    _META_KEYS: ClassVar[frozenset[str]] = frozenset(
        {
            "periode",
            "agent_groupe_agent",
            "noms_de_mesures",
            "valeurs_de_mesures",
        }
    )

    @classmethod
    def resolve(cls, normalized_key: str) -> tuple[str, str] | None:
        """Resout une cle normalisee.

        :param normalized_key: Cle issue de ``HeaderNormalizer``.
        :returns: ``(field_name, kind)`` ou ``None`` si inconnue.
        :spec: FEAT-009.1
        """
        return cls._MAP.get(normalized_key)

    @classmethod
    def is_meta_column(cls, normalized_key: str) -> bool:
        """Indique si la colonne est structurelle (pas une mesure).

        :param normalized_key: Cle normalisee.
        :returns: True si colonne meta.
        """
        return normalized_key in cls._META_KEYS
