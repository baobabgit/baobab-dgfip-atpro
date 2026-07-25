"""Package database infrastructure (engine, sessions, base ORM).

:spec: FEAT-016.1
"""

from __future__ import annotations

from atpro.infrastructure.database.alembic_config_factory import AlembicConfigFactory
from atpro.infrastructure.database.base import Base
from atpro.infrastructure.database.constraint_naming_convention import (
    ConstraintNamingConvention,
)
from atpro.infrastructure.database.engine_factory import EngineFactory
from atpro.infrastructure.database.session import SessionFactory
from atpro.infrastructure.database.unit_of_work import SqlAlchemyUnitOfWork
from atpro.infrastructure.database.unit_of_work_error import (
    UnitOfWorkAlreadyCommittedError,
    UnitOfWorkClosedError,
    UnitOfWorkError,
)

__all__: list[str] = [
    "AlembicConfigFactory",
    "Base",
    "ConstraintNamingConvention",
    "EngineFactory",
    "SessionFactory",
    "SqlAlchemyUnitOfWork",
    "UnitOfWorkAlreadyCommittedError",
    "UnitOfWorkClosedError",
    "UnitOfWorkError",
]
