"""Tests de FileSchema."""

from __future__ import annotations

import pytest

from atpro.domain.enums import ImportFileType, SchemaVersion
from atpro.domain.exceptions import DomainError
from atpro.parser.schemas.file_schema import FileSchema


class TestFileSchema:
    def test_FEAT_002_3_rejects_empty_required(self) -> None:
        with pytest.raises(DomainError):
            FileSchema(
                schema_id="x",
                file_type=ImportFileType.TICKETS,
                schema_version=SchemaVersion.V1,
                required_columns=frozenset(),
            )

    def test_FEAT_002_3_rejects_blank_schema_id(self) -> None:
        with pytest.raises(DomainError):
            FileSchema(
                schema_id="  ",
                file_type=ImportFileType.TICKETS,
                schema_version=SchemaVersion.V1,
                required_columns=frozenset({"a"}),
            )
