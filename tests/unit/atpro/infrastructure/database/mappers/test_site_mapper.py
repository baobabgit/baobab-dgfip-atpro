"""Tests unitaires de ``SiteMapper``.

:spec: FEAT-018.1
"""

from __future__ import annotations

from datetime import UTC, datetime

from atpro.domain.sites.site import Site
from atpro.infrastructure.database.mappers.site_mapper import SiteMapper
from atpro.infrastructure.database.models.site_model import SiteModel


class TestSiteMapper:
    def test_FEAT_018_1_roundtrip_site(self) -> None:
        now = datetime(2026, 1, 1, tzinfo=UTC)
        site = Site(
            id="s1",
            code="PAR",
            name="Paris",
            normalized_name="paris",
            active=True,
            created_at=now,
            updated_at=now,
            source_import_batch_id=None,
            line_fingerprint="fp",
        )
        mapper = SiteMapper()
        row = mapper.to_model(site)
        assert isinstance(row, SiteModel)
        restored = mapper.to_domain(row)
        assert restored == site
