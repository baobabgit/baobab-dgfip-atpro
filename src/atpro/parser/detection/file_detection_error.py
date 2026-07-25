"""Exceptions du sous-package detection.

:spec: FEAT-002.1
"""

from __future__ import annotations


class FileDetectionError(Exception):
    """Erreur fatale lors de l'inspection d'un fichier.

    :param code: Code stable (tests / CLI).
    :param message: Message comprehensible.
    :spec: FEAT-002.1
    """

    def __init__(self, code: str, message: str) -> None:
        """Initialise l'erreur de detection.

        :param code: Code stable.
        :param message: Description.
        """
        super().__init__(message)
        self.code = code
        self.message = message
