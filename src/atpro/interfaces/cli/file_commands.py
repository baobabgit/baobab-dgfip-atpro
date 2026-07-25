"""Groupe de commandes Typer ``file``.

:spec: FEAT-002.5
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from atpro.interfaces.cli.file_cli_service import FileCliService

file_app = typer.Typer(
    name="file",
    help="Inspecter, valider et previsualiser des fichiers CSV AT Pro.",
    no_args_is_help=True,
)

_service = FileCliService()


def configure_service(service: FileCliService) -> None:
    """Remplace le service CLI (tests).

    :param service: Service injecte.
    :spec: FEAT-002.5
    """
    global _service
    _service = service


@file_app.command("inspect")
def inspect_command(
    path: Annotated[
        Path,
        typer.Argument(exists=False, help="Chemin du fichier CSV."),
    ],
    as_json: Annotated[
        bool,
        typer.Option("--json", help="Sortie JSON."),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", help="Details supplementaires."),
    ] = False,
) -> None:
    """Inspecte un fichier CSV (type, schema, encodage).

    :spec: FEAT-002.5
    """
    outcome = _service.inspect(path, as_json=as_json, verbose=verbose)
    if outcome.text:
        typer.echo(outcome.text)
    raise typer.Exit(code=int(outcome.exit_code))


@file_app.command("validate")
def validate_command(
    path: Annotated[
        Path,
        typer.Argument(exists=False, help="Chemin du fichier CSV."),
    ],
    as_json: Annotated[
        bool,
        typer.Option("--json", help="Sortie JSON."),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", help="Details supplementaires."),
    ] = False,
) -> None:
    """Valide un fichier CSV via le parseur.

    :spec: FEAT-002.5
    """
    outcome = _service.validate(path, as_json=as_json, verbose=verbose)
    if outcome.text:
        typer.echo(outcome.text)
    raise typer.Exit(code=int(outcome.exit_code))


@file_app.command("preview")
def preview_command(
    path: Annotated[
        Path,
        typer.Argument(exists=False, help="Chemin du fichier CSV."),
    ],
    limit: Annotated[
        int,
        typer.Option("--limit", help="Nombre max d'enregistrements."),
    ] = 10,
    as_json: Annotated[
        bool,
        typer.Option("--json", help="Sortie JSON."),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", help="Details supplementaires."),
    ] = False,
) -> None:
    """Previsualise les premiers enregistrements d'un fichier CSV.

    :spec: FEAT-002.5
    """
    outcome = _service.preview(path, limit=limit, as_json=as_json, verbose=verbose)
    if outcome.text:
        typer.echo(outcome.text)
    raise typer.Exit(code=int(outcome.exit_code))
