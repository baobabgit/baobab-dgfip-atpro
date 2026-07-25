"""Implementation SQLAlchemy de la Unit of Work.

:spec: FEAT-016.2
"""

from __future__ import annotations

from types import TracebackType
from typing import Self

from sqlalchemy.orm import Session

from atpro.application.ports.unit_of_work import UnitOfWork
from atpro.infrastructure.database.session import SessionFactory
from atpro.infrastructure.database.unit_of_work_error import (
    UnitOfWorkAlreadyCommittedError,
    UnitOfWorkClosedError,
)


class SqlAlchemyUnitOfWork(UnitOfWork):
    """Unit of Work transactionnelle basee sur une session SQLAlchemy.

    Les repositories seront exposes ici lorsqu'ils seront disponibles
    (BL-030+). La session reste un detail d'infrastructure.

    :spec: FEAT-016.2
    """

    def __init__(self, session_factory: SessionFactory) -> None:
        """Initialise la UoW avec une fabrique de sessions.

        :param session_factory: Fabrique injectee (engine deja construit).
        """
        self._session_factory = session_factory
        self._session: Session | None = None
        self._committed = False
        self._closed = False

    @property
    def session(self) -> Session:
        """Session courante (usage infrastructure / tests uniquement).

        :returns: Session SQLAlchemy active.
        :rtype: Session
        :raises UnitOfWorkClosedError: Si aucune session n'est ouverte.
        """
        if self._session is None or self._closed:
            raise UnitOfWorkClosedError(
                "Unit of Work fermee ou non entree : session indisponible."
            )
        return self._session

    def __enter__(self) -> Self:
        """Ouvre une session et demarre le cycle de vie.

        :returns: Self.
        :raises UnitOfWorkClosedError: Si reutilisation apres fermeture.
        """
        if self._closed:
            raise UnitOfWorkClosedError(
                "Unit of Work deja fermee : creer une nouvelle instance."
            )
        if self._session is not None:
            raise UnitOfWorkClosedError(
                "Unit of Work deja ouverte : reutilisation invalide."
            )
        self._session = self._session_factory.create_session()
        self._committed = False
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """Rollback si exception ou commit absent, puis ferme.

        :param exc_type: Type d'exception eventuelle.
        :param exc: Exception eventuelle.
        :param tb: Traceback eventuel.
        """
        try:
            if exc_type is not None or not self._committed:
                self.rollback()
        finally:
            self.close()

    def commit(self) -> None:
        """Valide la transaction.

        :raises UnitOfWorkClosedError: Si fermee.
        :raises UnitOfWorkAlreadyCommittedError: Si deja committee.
        """
        session = self.session
        if self._committed:
            raise UnitOfWorkAlreadyCommittedError(
                "Commit refuse : transaction deja validee."
            )
        session.commit()
        self._committed = True

    def rollback(self) -> None:
        """Annule la transaction si une session est encore ouverte."""
        if self._session is None or self._closed:
            return
        self._session.rollback()
        self._committed = False

    def close(self) -> None:
        """Ferme la session courante."""
        if self._session is not None and not self._closed:
            self._session.close()
        self._session = None
        self._closed = True
