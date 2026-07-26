"""Repository SQLAlchemy pour les sites.

:spec: FEAT-018.1
"""

from __future__ import annotations

from dataclasses import replace

from sqlalchemy import select
from sqlalchemy.orm import Session

from atpro.application.ports.repository_write_outcome import RepositoryWriteOutcome
from atpro.application.ports.repository_write_result import RepositoryWriteResult
from atpro.application.ports.site_repository import SiteRepository
from atpro.domain.sites.site import Site
from atpro.infrastructure.database.mappers.site_mapper import SiteMapper
from atpro.infrastructure.database.models.site_model import SiteModel
from atpro.parser.normalizers.site_name_normalizer import SiteNameNormalizer


class SqlAlchemySiteRepository(SiteRepository):
    """Implementation SQLAlchemy de :class:`SiteRepository`.

    :spec: FEAT-018.1
    """

    def __init__(
        self,
        session: Session,
        *,
        mapper: SiteMapper | None = None,
        name_normalizer: SiteNameNormalizer | None = None,
    ) -> None:
        """Injecte session et collaborateurs.

        :param session: Session SQLAlchemy active.
        :param mapper: Mapper domaine/ORM.
        :param name_normalizer: Normaliseur de noms de sites.
        """
        self._session = session
        self._mapper = mapper or SiteMapper()
        self._name_normalizer = name_normalizer or SiteNameNormalizer()

    def add(self, site: Site) -> RepositoryWriteResult[Site]:
        """Cree ou reconcilie un site.

        :param site: Site domaine.
        :returns: Resultat explicite.
        """
        normalized = self._name_normalizer.normalize(site.name).normalized_value
        candidate = replace(site, normalized_name=normalized)

        existing = (
            self.get_by_id(candidate.id)
            or self.get_by_code(candidate.code)
            or self.get_by_normalized_name(candidate.normalized_name)
        )
        if existing is not None:
            if self._is_same_content(existing, candidate):
                return RepositoryWriteResult(
                    outcome=RepositoryWriteOutcome.EXISTING,
                    entity=existing,
                )
            return RepositoryWriteResult(
                outcome=RepositoryWriteOutcome.CONFLICT,
                entity=existing,
                message=(
                    "Conflit de cle metier site "
                    f"(code={candidate.code!r}, "
                    f"normalized_name={candidate.normalized_name!r})."
                ),
            )

        self._session.add(self._mapper.to_model(candidate))
        self._session.flush()
        return RepositoryWriteResult(
            outcome=RepositoryWriteOutcome.CREATED,
            entity=candidate,
        )

    def get_by_id(self, site_id: str) -> Site | None:
        """Recherche par identifiant.

        :param site_id: Identifiant.
        :returns: Site ou ``None``.
        """
        row = self._session.get(SiteModel, site_id)
        return self._mapper.to_domain(row) if row is not None else None

    def get_by_code(self, code: str) -> Site | None:
        """Recherche par code.

        :param code: Code site.
        :returns: Site ou ``None``.
        """
        statement = select(SiteModel).where(SiteModel.code == code)
        row = self._session.scalars(statement).first()
        return self._mapper.to_domain(row) if row is not None else None

    def get_by_normalized_name(self, normalized_name: str) -> Site | None:
        """Recherche par nom canonique.

        :param normalized_name: Nom normalise.
        :returns: Site ou ``None``.
        """
        statement = select(SiteModel).where(
            SiteModel.normalized_name == normalized_name
        )
        row = self._session.scalars(statement).first()
        return self._mapper.to_domain(row) if row is not None else None

    def list(self, *, limit: int = 100, offset: int = 0) -> list[Site]:
        """Liste bornee.

        :param limit: Nombre max.
        :param offset: Decalage.
        :returns: Sites.
        """
        statement = (
            select(SiteModel).order_by(SiteModel.code).offset(offset).limit(limit)
        )
        return [self._mapper.to_domain(row) for row in self._session.scalars(statement)]

    @staticmethod
    def _is_same_content(existing: Site, candidate: Site) -> bool:
        """Compare le contenu metier (hors timestamps / provenance).

        :param existing: Site en base.
        :param candidate: Site candidat.
        :returns: ``True`` si contenu equivalent.
        """
        return (
            existing.code == candidate.code
            and existing.name == candidate.name
            and existing.normalized_name == candidate.normalized_name
            and existing.active == candidate.active
        )
