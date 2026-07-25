"""Resultat d'import des activites agents.

:spec: FEAT-008.1
:spec: FEAT-009.1
"""

from __future__ import annotations

from dataclasses import dataclass

from atpro.domain.activities.agent_daily_activity import AgentDailyActivity
from atpro.parser.results.import_error import ImportError
from atpro.parser.results.import_warning import ImportWarning


@dataclass(frozen=True, slots=True)
class ActivityImportResult:
    """Activites produites avec diagnostics.

    :param activities: Activites journalieres construites.
    :param errors: Erreurs bloquantes.
    :param warnings: Avertissements.
    :spec: FEAT-008.1
    :spec: FEAT-009.1
    """

    activities: tuple[AgentDailyActivity, ...]
    errors: tuple[ImportError, ...] = ()
    warnings: tuple[ImportWarning, ...] = ()
