"""Tests de SchemaMatch."""

from __future__ import annotations

from atpro.domain.enums import ImportFileType, SchemaVersion
from atpro.parser.schemas.schema_match import SchemaMatch


class TestSchemaMatch:
    def test_FEAT_002_3_to_dict(self) -> None:
        match = SchemaMatch(
            schema_id="tickets_reduced",
            file_type=ImportFileType.TICKETS,
            schema_version=SchemaVersion.V1,
            score=8.0,
            confidence=1.0,
            matched_required=("numero_ticket",),
            missing_required=(),
            extra_columns=("foo",),
        )
        data = match.to_dict()
        assert data["file_type"] == "tickets"
        assert data["extra_columns"] == ["foo"]
