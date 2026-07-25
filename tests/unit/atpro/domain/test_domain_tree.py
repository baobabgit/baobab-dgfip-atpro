"""Tests d'import de l'arborescence domaine."""

from __future__ import annotations

import ast
from pathlib import Path

import atpro.domain
from atpro.domain.exceptions import DomainError

FORBIDDEN_IMPORTS = frozenset(
    {
        "sqlalchemy",
        "fastapi",
        "typer",
        "polars",
        "quarkdown",
        "django",
        "flask",
    }
)


class TestDomainTree:
    """Verification de l'arborescence domaine (BL-003)."""

    def test_FEAT_005_1_domain_packages_importable(self) -> None:
        """Les sous-packages domaine sont importables."""
        assert atpro.domain.agents.__name__ == "atpro.domain.agents"
        assert atpro.domain.sites.__name__ == "atpro.domain.sites"
        assert atpro.domain.calls.__name__ == "atpro.domain.calls"
        assert atpro.domain.tickets.__name__ == "atpro.domain.tickets"
        assert atpro.domain.activities.__name__ == "atpro.domain.activities"
        assert atpro.domain.imports.__name__ == "atpro.domain.imports"
        assert atpro.domain.enums.__name__ == "atpro.domain.enums"
        assert atpro.domain.exceptions.__name__ == "atpro.domain.exceptions"
        assert atpro.domain.value_objects.__name__ == "atpro.domain.value_objects"

    def test_FEAT_005_1_domain_error_usable(self) -> None:
        """DomainError est instanciable."""
        error = DomainError("echec")
        assert str(error) == "echec"
        assert error.message == "echec"

    def test_FEAT_005_1_no_infrastructure_imports_in_domain(self) -> None:
        """Aucun import infrastructure dans domain/."""
        domain_root = Path(atpro.domain.__file__).resolve().parent
        for path in domain_root.rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        root = alias.name.split(".", maxsplit=1)[0]
                        assert root not in FORBIDDEN_IMPORTS, path
                elif isinstance(node, ast.ImportFrom) and node.module:
                    root = node.module.split(".", maxsplit=1)[0]
                    assert root not in FORBIDDEN_IMPORTS, path
