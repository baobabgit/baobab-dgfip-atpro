"""Tests unitaires de ``Base``.

:spec: FEAT-016.1
"""

from __future__ import annotations

from atpro.infrastructure.database.base import Base
from atpro.infrastructure.database.constraint_naming_convention import (
    ConstraintNamingConvention,
)


class TestBase:
    def test_FEAT_016_1_metadata_utilise_naming_convention(self) -> None:
        assert Base.metadata.naming_convention == (ConstraintNamingConvention.mapping())
