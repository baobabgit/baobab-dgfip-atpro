"""Application Typer racine ``atpro``.

:spec: FEAT-002.5
"""

from __future__ import annotations

import typer

from atpro.interfaces.cli.file_commands import file_app

app = typer.Typer(
    name="atpro",
    help="CLI AT Pro Pilotage — inspection et validation de fichiers CSV.",
    no_args_is_help=True,
)
app.add_typer(file_app, name="file")


def run() -> None:
    """Point d'entree console_scripts ``atpro``.

    :spec: FEAT-002.5
    """
    app()
