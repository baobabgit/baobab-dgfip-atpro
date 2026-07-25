"""Tests d'import des modules enums reserves."""

from __future__ import annotations

from atpro.domain.enums import (
    CallDirection,
    ImportFileType,
    ImportSeverity,
    ParseStatus,
    PeriodType,
    SchemaVersion,
    ScopeType,
)


class TestEnumModules:
    """Les modules enums exposent les classes attendues (BL-004)."""

    def test_FEAT_005_2_enum_modules_export_classes(self) -> None:
        """Chaque enum partagee est disponible."""
        assert PeriodType.DAY
        assert ScopeType.SITE
        assert ImportFileType.TICKETS
        assert CallDirection.INCOMING
        assert ImportSeverity.WARNING
        assert ParseStatus.PARTIAL
        assert SchemaVersion.UNKNOWN
