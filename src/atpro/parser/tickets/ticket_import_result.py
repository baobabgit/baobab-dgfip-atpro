"""Resultat d'import tickets.

:spec: FEAT-007.1
"""

from __future__ import annotations

from dataclasses import dataclass

from atpro.domain.tickets.ticket import Ticket
from atpro.parser.normalizers.normalized_identity import NormalizedIdentity
from atpro.parser.results.import_error import ImportError
from atpro.parser.results.import_warning import ImportWarning


@dataclass(frozen=True, slots=True)
class TicketImportResult:
    """Tickets produits avec diagnostics et identites.

    :param tickets: Tickets construits.
    :param agent_identities: Identites agents normalisees.
    :param site_identities: Identites sites normalisees.
    :param errors: Erreurs bloquantes.
    :param warnings: Avertissements.
    :spec: FEAT-007.1
    """

    tickets: tuple[Ticket, ...]
    agent_identities: tuple[NormalizedIdentity, ...] = ()
    site_identities: tuple[NormalizedIdentity, ...] = ()
    errors: tuple[ImportError, ...] = ()
    warnings: tuple[ImportWarning, ...] = ()
