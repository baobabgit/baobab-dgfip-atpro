"""Tests d'import des modules enums reserves."""

from __future__ import annotations

import atpro.domain.enums.call_direction as call_direction
import atpro.domain.enums.import_file_type as import_file_type
import atpro.domain.enums.import_severity as import_severity
import atpro.domain.enums.parse_status as parse_status
import atpro.domain.enums.period_type as period_type
import atpro.domain.enums.schema_version as schema_version
import atpro.domain.enums.scope_type as scope_type


class TestEnumModules:
    """Les modules enums existent et sont importables (BL-003)."""

    def test_FEAT_005_2_enum_modules_exist(self) -> None:
        """Chaque module enum partage est present."""
        modules = (
            period_type,
            scope_type,
            import_file_type,
            call_direction,
            import_severity,
            parse_status,
            schema_version,
        )
        for module in modules:
            assert module.__all__ == []
