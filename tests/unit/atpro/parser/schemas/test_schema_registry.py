"""Tests du registre de schemas."""

from __future__ import annotations

from atpro.parser.schemas.schema_registry import SchemaRegistry


class TestSchemaRegistry:
    def test_FEAT_002_3_default_catalog_size(self) -> None:
        registry = SchemaRegistry()
        ids = {schema.schema_id for schema in registry.all()}
        assert "incoming_calls_v1" in ids
        assert "outgoing_calls_v1" in ids
        assert "tickets_long" in ids
        assert "tickets_reduced" in ids
        assert "activities_wide" in ids
        assert "activities_long" in ids

    def test_FEAT_002_3_get_by_id(self) -> None:
        registry = SchemaRegistry()
        assert registry.get("tickets_reduced") is not None
        assert registry.get("missing") is None
