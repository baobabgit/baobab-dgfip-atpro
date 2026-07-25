"""Erreur de base du domaine atpro.

:spec: FEAT-005.1
"""

from __future__ import annotations


class DomainError(Exception):
    """Exception de base pour les erreurs metier du domaine.

    :param message: Description de l'erreur.
    :type message: str
    :spec: FEAT-005.1
    """

    def __init__(self, message: str) -> None:
        """Initialise l'erreur domaine.

        :param message: Description de l'erreur.
        :type message: str
        """
        super().__init__(message)
        self.message = message
