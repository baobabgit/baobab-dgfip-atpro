"""Erreur structuree de normalisation.

:spec: FEAT-005.3
"""

from __future__ import annotations


class NormalizationError(Exception):
    """Echec de conversion d'une valeur brute.

    Destinee a etre capturee par les readers / CLI, jamais propagee brute.

    :param code: Code stable.
    :param message: Message localise.
    :param raw_value: Valeur source (deja masquee si sensible).
    :param column: Colonne optionnelle.
    :spec: FEAT-005.3
    """

    def __init__(
        self,
        code: str,
        message: str,
        *,
        raw_value: str | None = None,
        column: str | None = None,
    ) -> None:
        """Initialise l'erreur.

        :param code: Code stable.
        :param message: Description.
        :param raw_value: Valeur brute.
        :param column: Nom de colonne.
        """
        super().__init__(message)
        self.code = code
        self.message = message
        self.raw_value = raw_value
        self.column = column
