"""Modeles ORM infrastructure (imports, referentiels et metier v0.2.0).

:spec: FEAT-017.2
"""

from __future__ import annotations

from atpro.infrastructure.database.models.agent_alias_model import AgentAliasModel
from atpro.infrastructure.database.models.agent_daily_activity_model import (
    AgentDailyActivityModel,
)
from atpro.infrastructure.database.models.agent_model import AgentModel
from atpro.infrastructure.database.models.agent_site_assignment_model import (
    AgentSiteAssignmentModel,
)
from atpro.infrastructure.database.models.call_model import CallModel
from atpro.infrastructure.database.models.call_segment_model import CallSegmentModel
from atpro.infrastructure.database.models.import_batch_model import ImportBatchModel
from atpro.infrastructure.database.models.import_rejected_row_model import (
    ImportRejectedRowModel,
)
from atpro.infrastructure.database.models.site_model import SiteModel
from atpro.infrastructure.database.models.ticket_model import TicketModel

__all__: list[str] = [
    "AgentAliasModel",
    "AgentDailyActivityModel",
    "AgentModel",
    "AgentSiteAssignmentModel",
    "CallModel",
    "CallSegmentModel",
    "ImportBatchModel",
    "ImportRejectedRowModel",
    "SiteModel",
    "TicketModel",
]
