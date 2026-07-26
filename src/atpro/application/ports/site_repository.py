"""Port repository Site.

:spec: FEAT-018.1
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from atpro.application.ports.repository_write_result import RepositoryWriteResult
from atpro.domain.sites.site import Site


class SiteRepository(ABC):
    """Persistance et consultation des sites (sans objets ORM).

    :spec: FEAT-018.1
    """

    @abstractmethod
    def add(self, site: Site) -> RepositoryWriteResult[Site]:
        """Cree ou reconcilie un site de facon idempotente.

        :param site: Site domaine.
        :returns: Resultat explicite (created / existing / conflict).
        """

    @abstractmethod
    def get_by_id(self, site_id: str) -> Site | None:
        """Recherche par identifiant interne.

        :param site_id: Identifiant.
        :returns: Site ou ``None``.
        """

    @abstractmethod
    def get_by_code(self, code: str) -> Site | None:
        """Recherche par code site.

        :param code: Code metier.
        :returns: Site ou ``None``.
        """

    @abstractmethod
    def get_by_normalized_name(self, normalized_name: str) -> Site | None:
        """Recherche par nom canonique.

        :param normalized_name: Nom normalise.
        :returns: Site ou ``None``.
        """

    @abstractmethod
    def list(self, *, limit: int = 100, offset: int = 0) -> list[Site]:
        """Liste bornee (CLI), y compris sites inactifs.

        :param limit: Nombre max.
        :param offset: Decalage.
        :returns: Sites.
        """
