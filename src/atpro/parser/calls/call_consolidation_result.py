"""Resultat de consolidation d'appels.

:spec: FEAT-005.4
"""

from __future__ import annotations

from dataclasses import dataclass

from atpro.domain.calls.call import Call
from atpro.domain.calls.call_segment import CallSegment
from atpro.parser.results.import_error import ImportError
from atpro.parser.results.import_warning import ImportWarning


@dataclass(frozen=True, slots=True)
class CallConsolidationResult:
    """Appels et segments produits avec diagnostics.

    :param calls: Appels consolides.
    :param segments: Segments associes.
    :param errors: Erreurs bloquantes.
    :param warnings: Avertissements.
    :spec: FEAT-005.4
    """

    calls: tuple[Call, ...]
    segments: tuple[CallSegment, ...]
    errors: tuple[ImportError, ...] = ()
    warnings: tuple[ImportWarning, ...] = ()
