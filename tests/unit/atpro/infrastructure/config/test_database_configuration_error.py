"""Tests unitaires de ``DatabaseConfigurationError``.

:spec: FEAT-015.2
"""

from __future__ import annotations

from atpro.infrastructure.config.database_configuration_error import (
    DatabaseConfigurationError,
)


class TestDatabaseConfigurationError:
    def test_FEAT_015_2_message_accessible(self) -> None:
        error = DatabaseConfigurationError("config incomplete")
        assert str(error) == "config incomplete"
        assert error.message == "config incomplete"
