"""Tests des messages de colonnes manquantes."""

from __future__ import annotations

from atpro.parser.schemas.missing_columns_message import MissingColumnsMessage


class TestMissingColumnsMessage:
    def test_FEAT_002_3_builds_warning(self) -> None:
        warning = MissingColumnsMessage().build(
            schema_id="tickets_reduced",
            missing_required=("statut_ticket",),
        )
        assert warning is not None
        assert warning.issue.code == "SCHEMA_MISSING_COLUMNS"
        assert "statut_ticket" in warning.issue.message

    def test_FEAT_002_3_none_when_complete(self) -> None:
        assert (
            MissingColumnsMessage().build(
                schema_id="x",
                missing_required=(),
            )
            is None
        )
