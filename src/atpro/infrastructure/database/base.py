"""Base declarative SQLAlchemy pour les modeles ORM atpro.

:spec: FEAT-016.1
"""

from __future__ import annotations

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from atpro.infrastructure.database.constraint_naming_convention import (
    ConstraintNamingConvention,
)


class Base(DeclarativeBase):
    """Base ORM declarative partagee par les tables infrastructure.

    Aucune connexion n'est ouverte a l'import de ce module.

    :spec: FEAT-016.1
    """

    metadata = MetaData(naming_convention=ConstraintNamingConvention.mapping())
