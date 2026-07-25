"""Conventions de nommage des contraintes SQLAlchemy.

:spec: FEAT-016.1
"""

from __future__ import annotations


class ConstraintNamingConvention:
    """Conventions de nommage stables pour indexes et contraintes.

    :spec: FEAT-016.1
    """

    @staticmethod
    def mapping() -> dict[str, str]:
        """Retourne le mapping ``MetaData.naming_convention``.

        :returns: Dictionnaire de conventions SQLAlchemy.
        :rtype: dict[str, str]
        """
        return {
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": ("fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"),
            "pk": "pk_%(table_name)s",
        }
