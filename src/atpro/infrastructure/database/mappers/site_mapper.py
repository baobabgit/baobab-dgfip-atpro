"""Mapper Site domaine ↔ ORM.

:spec: FEAT-018.1
"""

from __future__ import annotations

from atpro.domain.sites.site import Site
from atpro.infrastructure.database.models.site_model import SiteModel


class SiteMapper:
    """Conversion bidirectionnelle Site / SiteModel.

    :spec: FEAT-018.1
    """

    def to_domain(self, row: SiteModel) -> Site:
        """ORM vers domaine.

        :param row: Ligne ORM.
        :returns: Site domaine.
        """
        return Site(
            id=row.id,
            code=row.code,
            name=row.name,
            normalized_name=row.normalized_name,
            active=row.active,
            created_at=row.created_at,
            updated_at=row.updated_at,
            source_import_batch_id=row.source_import_batch_id,
            line_fingerprint=row.line_fingerprint,
        )

    def to_model(self, site: Site) -> SiteModel:
        """Domaine vers ORM.

        :param site: Site domaine.
        :returns: Ligne ORM non attachee.
        """
        return SiteModel(
            id=site.id,
            code=site.code,
            name=site.name,
            normalized_name=site.normalized_name,
            active=site.active,
            created_at=site.created_at,
            updated_at=site.updated_at,
            source_import_batch_id=site.source_import_batch_id,
            line_fingerprint=site.line_fingerprint,
        )
