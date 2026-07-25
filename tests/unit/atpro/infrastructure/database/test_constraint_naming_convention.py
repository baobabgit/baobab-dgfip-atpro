"""Tests unitaires de ``ConstraintNamingConvention``.

:spec: FEAT-016.1
"""

from __future__ import annotations

from atpro.infrastructure.database.constraint_naming_convention import (
    ConstraintNamingConvention,
)


class TestConstraintNamingConvention:
    def test_FEAT_016_1_mapping_cles_attendues(self) -> None:
        mapping = ConstraintNamingConvention.mapping()
        assert set(mapping) == {"ix", "uq", "ck", "fk", "pk"}
        assert "pk_%(table_name)s" == mapping["pk"]
        assert "uq_%(table_name)s_%(column_0_name)s" == mapping["uq"]
