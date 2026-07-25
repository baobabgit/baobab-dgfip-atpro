"""Erreur de configuration infrastructure.

:spec: FEAT-015.2
"""

from __future__ import annotations


class DatabaseConfigurationError(Exception):
    """Configuration PostgreSQL incomplete ou invalide.

    :param message: Description lisible de l'erreur.
    :type message: str
    :spec: FEAT-015.2
    """

    def __init__(self, message: str) -> None:
        """Initialise l'erreur de configuration.

        :param message: Description lisible de l'erreur.
        :type message: str
        """
        super().__init__(message)
        self.message = message
