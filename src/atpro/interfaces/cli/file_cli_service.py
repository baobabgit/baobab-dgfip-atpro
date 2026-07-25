"""Service CLI pour les commandes ``file``.

:spec: FEAT-002.5
"""

from __future__ import annotations

from pathlib import Path

from atpro.interfaces.cli.cli_outcome import CliOutcome
from atpro.interfaces.cli.cli_presenter import CliPresenter
from atpro.interfaces.cli.exit_code import ExitCode
from atpro.parser.detection.file_detection_error import FileDetectionError
from atpro.parser.parse_file_use_case import ParseFileUseCase


class FileCliService:
    """Delegue au cas d'usage de parsing et presente le resultat.

    Aucune logique metier : orchestration CLI uniquement.

    :param use_case: Cas d'usage ``ParseFileUseCase``.
    :param presenter: Formateur de sortie.
    :spec: FEAT-002.5
    """

    def __init__(
        self,
        *,
        use_case: ParseFileUseCase | None = None,
        presenter: CliPresenter | None = None,
    ) -> None:
        """Injecte les collaborateurs (tests).

        :param use_case: Orchestrateur de parsing.
        :param presenter: Presentateur CLI.
        """
        self._use_case = use_case or ParseFileUseCase()
        self._presenter = presenter or CliPresenter()

    def inspect(
        self,
        path: Path,
        *,
        as_json: bool = False,
        verbose: bool = False,
    ) -> CliOutcome:
        """Execute ``file inspect``.

        :param path: Chemin du fichier.
        :param as_json: Sortie JSON.
        :param verbose: Details supplementaires.
        :returns: Texte et code de sortie.
        :spec: FEAT-002.5
        """
        try:
            inspection = self._use_case.inspect(path)
        except FileDetectionError as exc:
            return CliOutcome(
                exit_code=ExitCode.MISSING_OR_UNREADABLE,
                text=self._presenter.format_detection_error(
                    exc.code, exc.message, as_json=as_json
                ),
            )
        except Exception as exc:
            return CliOutcome(
                exit_code=ExitCode.TECHNICAL_ERROR,
                text=self._presenter.format_technical_error(str(exc), as_json=as_json),
            )
        return CliOutcome(
            exit_code=ExitCode.SUCCESS,
            text=self._presenter.format_inspection(
                inspection, as_json=as_json, verbose=verbose
            ),
        )

    def validate(
        self,
        path: Path,
        *,
        as_json: bool = False,
        verbose: bool = False,
    ) -> CliOutcome:
        """Execute ``file validate``.

        :param path: Chemin du fichier.
        :param as_json: Sortie JSON.
        :param verbose: Details supplementaires.
        :returns: Texte et code de sortie.
        :spec: FEAT-002.5
        """
        try:
            result = self._use_case.validate(path)
        except Exception as exc:
            return CliOutcome(
                exit_code=ExitCode.TECHNICAL_ERROR,
                text=self._presenter.format_technical_error(str(exc), as_json=as_json),
            )
        return CliOutcome(
            exit_code=ExitCode.from_parse_result(result),
            text=self._presenter.format_parse_result(
                result, as_json=as_json, verbose=verbose
            ),
        )

    def preview(
        self,
        path: Path,
        *,
        limit: int = 10,
        as_json: bool = False,
        verbose: bool = False,
    ) -> CliOutcome:
        """Execute ``file preview``.

        :param path: Chemin du fichier.
        :param limit: Nombre max d'enregistrements.
        :param as_json: Sortie JSON.
        :param verbose: Details supplementaires.
        :returns: Texte et code de sortie.
        :spec: FEAT-002.5
        """
        try:
            preview = self._use_case.preview(path, limit=limit)
        except Exception as exc:
            return CliOutcome(
                exit_code=ExitCode.TECHNICAL_ERROR,
                text=self._presenter.format_technical_error(str(exc), as_json=as_json),
            )
        return CliOutcome(
            exit_code=ExitCode.from_parse_preview(preview),
            text=self._presenter.format_preview(
                preview, as_json=as_json, verbose=verbose
            ),
        )
