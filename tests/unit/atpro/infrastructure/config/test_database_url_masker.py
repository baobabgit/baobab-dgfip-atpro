"""Tests unitaires de ``DatabaseUrlMasker``.

:spec: FEAT-015.2
"""

from __future__ import annotations

from atpro.infrastructure.config.database_url_masker import DatabaseUrlMasker


class TestDatabaseUrlMasker:
    def test_FEAT_015_2_masque_password_dans_url(self) -> None:
        masker = DatabaseUrlMasker()
        masked = masker.mask("postgresql+psycopg://alice:hunter2@host:5432/db")
        assert masked == "postgresql+psycopg://alice:***@host:5432/db"
        assert "hunter2" not in masked

    def test_FEAT_015_2_url_sans_password(self) -> None:
        masker = DatabaseUrlMasker()
        url = "postgresql+psycopg://alice@host:5432/db"
        assert masker.mask(url) == "postgresql+psycopg://alice:***@host:5432/db"

    def test_FEAT_015_2_url_sans_netloc_inchangee(self) -> None:
        masker = DatabaseUrlMasker()
        assert masker.mask("sqlite://") == "sqlite://"
