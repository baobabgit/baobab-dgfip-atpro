"""Validation structurelle du Compose PostgreSQL de developpement.

:spec: FEAT-015.1
"""

from __future__ import annotations

from pathlib import Path

import yaml


class TestPostgresCompose:
    def test_FEAT_015_1_compose_declare_postgres_17(self) -> None:
        root = Path(__file__).resolve().parents[4]
        compose_path = root / "compose.yml"
        data = yaml.safe_load(compose_path.read_text(encoding="utf-8"))
        postgres = data["services"]["postgres"]
        assert postgres["image"] == "postgres:17"
        assert "atpro_postgres_data" in str(postgres["volumes"])
        assert "healthcheck" in postgres
        assert "pg_isready" in " ".join(postgres["healthcheck"]["test"])
        env = postgres["environment"]
        assert "POSTGRES_PASSWORD" in env
        assert "changeme" not in str(env).lower()
        assert "production" not in str(env).lower()

    def test_FEAT_015_1_documentation_operations_presente(self) -> None:
        root = Path(__file__).resolve().parents[4]
        doc = (root / "docs/operations/database.md").read_text(encoding="utf-8")
        assert "docker compose up -d postgres" in doc
        assert "docker volume rm atpro_postgres_data" in doc
        assert "healthcheck" in doc.lower() or "pg_isready" in doc
