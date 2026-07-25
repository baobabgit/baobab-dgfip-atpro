"""Tests de DomainError."""

from __future__ import annotations

import pytest

from atpro.domain.exceptions.domain_error import DomainError


class TestDomainError:
    """Couverture de DomainError."""

    def test_FEAT_005_1_raise_domain_error(self) -> None:
        """DomainError peut etre levee et attrapee."""
        with pytest.raises(DomainError) as exc_info:
            raise DomainError("invalide")
        assert exc_info.value.message == "invalide"
