"""Resume quantitatif d'un parsing.

:spec: FEAT-003.1
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from atpro.domain.enums.parse_status import ParseStatus
from atpro.domain.exceptions.domain_error import DomainError


@dataclass(frozen=True, slots=True)
class ParseSummary:
    """Compteurs et statut global d'un parsing.

    :param status: Statut global.
    :param record_count: Nombre d'enregistrements produits.
    :param warning_count: Nombre d'avertissements.
    :param error_count: Nombre d'erreurs.
    :spec: FEAT-003.1
    """

    status: ParseStatus
    record_count: int
    warning_count: int
    error_count: int

    def __post_init__(self) -> None:
        """Valide les compteurs.

        :raises DomainError: Si un compteur est negatif.
        """
        for name, value in (
            ("record_count", self.record_count),
            ("warning_count", self.warning_count),
            ("error_count", self.error_count),
        ):
            if value < 0:
                raise DomainError(f"ParseSummary.{name} negatif")

    def to_dict(self) -> dict[str, Any]:
        """Serialise le resume.

        :returns: Dictionnaire JSON-compatible.
        """
        payload = asdict(self)
        payload["status"] = self.status.value
        return payload
