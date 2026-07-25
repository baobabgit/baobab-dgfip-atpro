"""Erreurs techniques de Unit of Work.

:spec: FEAT-016.2
"""

from __future__ import annotations


class UnitOfWorkError(Exception):
    """Erreur technique de cycle de vie Unit of Work.

    :param message: Description lisible.
    :type message: str
    :spec: FEAT-016.2
    """

    def __init__(self, message: str) -> None:
        """Initialise l'erreur.

        :param message: Description lisible.
        :type message: str
        """
        super().__init__(message)
        self.message = message


class UnitOfWorkClosedError(UnitOfWorkError):
    """Operation refusee car la Unit of Work est fermee.

    :spec: FEAT-016.2
    """


class UnitOfWorkAlreadyCommittedError(UnitOfWorkError):
    """Commit refuse car la transaction a deja ete validee.

    :spec: FEAT-016.2
    """
