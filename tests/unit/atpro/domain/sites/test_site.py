"""Tests du modele Site."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from atpro.domain.exceptions import DomainError
from atpro.domain.sites import Site


class TestSite:
    """Instanciation et validation de Site."""

    def test_FEAT_005_1_instantiate_site(self) -> None:
        now = datetime(2026, 1, 1, tzinfo=UTC)
        site = Site(
            id="s1",
            code="PAR",
            name="Paris",
            normalized_name="paris",
            active=True,
            created_at=now,
            updated_at=now,
            source_import_batch_id="batch-1",
            line_fingerprint="fp-1",
        )
        assert site.code == "PAR"
        assert site.source_import_batch_id == "batch-1"

    def test_FEAT_005_1_site_requires_id(self) -> None:
        now = datetime(2026, 1, 1, tzinfo=UTC)
        with pytest.raises(DomainError):
            Site(
                id=" ",
                code="PAR",
                name="Paris",
                normalized_name="paris",
                active=True,
                created_at=now,
                updated_at=now,
            )

    def test_FEAT_005_1_site_requires_code_and_name(self) -> None:
        now = datetime(2026, 1, 1, tzinfo=UTC)
        with pytest.raises(DomainError):
            Site(
                id="s1",
                code=" ",
                name="Paris",
                normalized_name="paris",
                active=True,
                created_at=now,
                updated_at=now,
            )
        with pytest.raises(DomainError):
            Site(
                id="s1",
                code="PAR",
                name=" ",
                normalized_name="paris",
                active=True,
                created_at=now,
                updated_at=now,
            )
