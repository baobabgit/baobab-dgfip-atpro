"""Fabrique de sessions SQLAlchemy injectables.

:spec: FEAT-016.1
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


class SessionFactory:
    """Fabrique de sessions non globales, injectables dans les repositories.

    Les transactions applicatives restent sous controle de la Unit of Work
    (FEAT-016.2). Ce helper fournit uniquement l'ouverture / fermeture et un
    scope de confort pour le CLI et les tests.

    :spec: FEAT-016.1
    """

    def __init__(self, engine: Engine) -> None:
        """Initialise la fabrique liee a un engine.

        :param engine: Engine SQLAlchemy deja construit.
        """
        self._sessionmaker: sessionmaker[Session] = sessionmaker(
            bind=engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def create_session(self) -> Session:
        """Ouvre une nouvelle session injectables.

        :returns: Session SQLAlchemy.
        :rtype: Session
        """
        return self._sessionmaker()

    @contextmanager
    def session_scope(self) -> Iterator[Session]:
        """Ouvre une session, commit si succes, rollback sinon, puis ferme.

        :yields: Session active.
        :rtype: Iterator[Session]
        """
        session = self.create_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
