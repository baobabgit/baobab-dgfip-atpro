"""Port applicatif Unit of Work.

:spec: FEAT-016.2
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self


class UnitOfWork(ABC):
    """Point d'entree transactionnel pour les cas d'usage.

    Les cas d'usage ne doivent pas manipuler une ``Session`` SQLAlchemy
    directement : ils passent par cette interface.

    :spec: FEAT-016.2
    """

    @abstractmethod
    def __enter__(self) -> Self:
        """Ouvre la transaction applicative.

        :returns: Instance prete a l'emploi.
        """

    @abstractmethod
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """Ferme la transaction (rollback si erreur ou commit absent).

        :param exc_type: Type d'exception eventuelle.
        :param exc: Exception eventuelle.
        :param tb: Traceback eventuel.
        """

    @abstractmethod
    def commit(self) -> None:
        """Valide explicitement la transaction courante."""

    @abstractmethod
    def rollback(self) -> None:
        """Annule la transaction courante."""

    @abstractmethod
    def close(self) -> None:
        """Ferme les ressources transactionnelles."""
