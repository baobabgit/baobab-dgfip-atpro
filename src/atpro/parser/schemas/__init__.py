"""Registre et detection de schemas CSV.

:spec: FEAT-002.3
"""

from __future__ import annotations

from atpro.parser.schemas.file_schema import FileSchema
from atpro.parser.schemas.missing_columns_message import MissingColumnsMessage
from atpro.parser.schemas.schema_detector import SchemaDetector
from atpro.parser.schemas.schema_match import SchemaMatch
from atpro.parser.schemas.schema_registry import SchemaRegistry

__all__ = [
    "FileSchema",
    "MissingColumnsMessage",
    "SchemaDetector",
    "SchemaMatch",
    "SchemaRegistry",
]
