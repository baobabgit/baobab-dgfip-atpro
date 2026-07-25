"""Tests des enumerations domaine."""

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


class TestDomainEnums:
    """Couverture des enums FEAT-005.2."""

    def test_FEAT_005_2_import_file_type_values(self) -> None:
        assert ImportFileType.INCOMING_CALLS == "incoming_calls"
        assert ImportFileType.UNKNOWN == "unknown"

    def test_FEAT_005_2_call_direction_values(self) -> None:
        assert CallDirection.INCOMING == "incoming"
        assert CallDirection.OUTGOING == "outgoing"

    def test_FEAT_005_2_parse_and_severity(self) -> None:
        assert ParseStatus.SUCCESS == "success"
        assert ImportSeverity.ERROR == "error"

    def test_FEAT_005_2_period_scope_schema(self) -> None:
        assert PeriodType.DAY == "day"
        assert ScopeType.AGENT == "agent"
        assert SchemaVersion.V1 == "v1"
