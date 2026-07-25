"""Modele Agent.

:spec: FEAT-005.1
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from atpro.domain.exceptions.domain_error import DomainError


@dataclass(frozen=True, slots=True)
class Agent:
    """Personne physique normalisee.

    :param id: Identifiant interne.
    :param first_name: Prenom.
    :param last_name: Nom.
    :param display_name: Nom affiche.
    :param normalized_identity: Identite normalisee.
    :param active: Indique si l'agent est actif.
    :param created_at: Horodatage de creation.
    :param updated_at: Horodatage de mise a jour.
    :param source_import_batch_id: Lot d'import d'origine (provenance).
    :param line_fingerprint: Empreinte de ligne source (provenance).
    :spec: FEAT-005.1
    """

    id: str
    first_name: str
    last_name: str
    display_name: str
    normalized_identity: str
    active: bool
    created_at: datetime
    updated_at: datetime
    source_import_batch_id: str | None = None
    line_fingerprint: str | None = None

    def __post_init__(self) -> None:
        """Valide les champs obligatoires.

        :raises DomainError: Si un champ obligatoire est vide.
        """
        if not self.id.strip():
            raise DomainError("Agent.id obligatoire")
        if not self.display_name.strip():
            raise DomainError("Agent.display_name obligatoire")
        if not self.normalized_identity.strip():
            raise DomainError("Agent.normalized_identity obligatoire")
