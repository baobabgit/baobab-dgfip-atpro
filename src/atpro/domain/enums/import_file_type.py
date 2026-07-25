"""Enumeration ``ImportFileType``.

:spec: FEAT-005.2
"""

from __future__ import annotations

from enum import StrEnum


class ImportFileType(StrEnum):
    """Type de fichier CSV detecte.

    :spec: FEAT-005.2
    """

    INCOMING_CALLS = "incoming_calls"
    OUTGOING_CALLS = "outgoing_calls"
    TICKETS = "tickets"
    AGENT_ACTIVITIES = "agent_activities"
    UNKNOWN = "unknown"
