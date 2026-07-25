"""Tests d'import du package atpro."""

from __future__ import annotations

import atpro
from atpro import domain


class TestAtproPackage:
    """Couverture minimale du package applicatif."""

    def test_FEAT_001_1_import_atpro(self) -> None:
        """Le package atpro est importable."""
        assert atpro.__version__ == "0.1.0"
        assert "__version__" in atpro.__all__
        assert "domain" in atpro.__all__
        assert domain.__name__ == "atpro.domain"
