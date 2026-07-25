"""Resultat d'une commande CLI.

:spec: FEAT-002.5
"""

from __future__ import annotations

from dataclasses import dataclass

from atpro.interfaces.cli.exit_code import ExitCode


@dataclass(frozen=True, slots=True)
class CliOutcome:
    """Resultat d'une commande CLI (texte + code de sortie).

    :param exit_code: Code FEAT-002.5.
    :param text: Sortie standard a afficher.
    :spec: FEAT-002.5
    """

    exit_code: ExitCode
    text: str
