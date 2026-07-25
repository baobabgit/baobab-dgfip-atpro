"""Modele Site.

:spec: FEAT-005.1
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from atpro.domain.exceptions.domain_error import DomainError


@dataclass(frozen=True, slots=True)
class Site:
    """Site de rattachement ou de traitement.

    :param id: Identifiant interne.
    :param code: Code site.
    :param name: Libelle affiche.
    :param normalized_name: Libelle normalise.
    :param active: Indique si le site est actif.
    :param created_at: Horodatage de creation.
    :param updated_at: Horodatage de mise a jour.
    :param source_import_batch_id: Lot d'import d'origine (provenance).
    :param line_fingerprint: Empreinte de ligne source (provenance).
    :spec: FEAT-005.1
    """

    id: str
    code: str
    name: str
    normalized_name: str
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
            raise DomainError("Site.id obligatoire")
        if not self.code.strip():
            raise DomainError("Site.code obligatoire")
        if not self.name.strip():
            raise DomainError("Site.name obligatoire")
