"""Validation optionnelle sur CSV reels de reference.

:spec: FEAT-013.1
"""

from __future__ import annotations

import pytest

from atpro.parser.detection.file_detection_error import FileDetectionError
from atpro.parser.parse_file_use_case import ParseFileUseCase
from atpro.testing.reference_data_locator import ReferenceDataLocator


def _safe_error_summary(code: str, message: str, column: str | None) -> str:
    """Resume d'erreur sans valeur brute sensible.

    :param code: Code d'issue.
    :param message: Message (deja masque cote parseur si sensible).
    :param column: Colonne optionnelle.
    :returns: Ligne de diagnostic.
    """
    col = f" col={column}" if column else ""
    return f"{code}{col}: {message}"


@pytest.mark.reference
class TestReferenceCsvOptional:
    """Tests marques ``reference`` — skip si env absent, fail si dossier vide.

    :spec: FEAT-013.1
    """

    def test_FEAT_013_1_reference_csv_inspect_and_validate(self) -> None:
        locator = ReferenceDataLocator()
        if not locator.is_configured():
            pytest.skip("ATPRO_REFERENCE_CSV_DIR absent")

        directory = locator.resolve_dir()
        assert directory is not None

        if locator.is_empty():
            pytest.fail(
                "dossier reference vide : validation non effectuee "
                f"(ATPRO_REFERENCE_CSV_DIR={directory})"
            )

        use_case = ParseFileUseCase()
        collected: list[str] = []

        for csv_path in locator.iter_csv_files():
            try:
                inspection = use_case.inspect(csv_path)
                detected = inspection.detected_type.value
            except FileDetectionError as exc:
                collected.append(
                    f"{csv_path.name}: detection {exc.code} ({exc.message})"
                )
                continue

            result = use_case.validate(csv_path)
            for err in result.errors:
                collected.append(
                    f"{csv_path.name} [{detected}] "
                    + _safe_error_summary(
                        err.issue.code,
                        err.issue.message,
                        err.issue.column,
                    )
                )

        if collected:
            # Noms de fichiers + codes uniquement — pas de raw_value.
            joined = "; ".join(collected)
            pytest.fail(f"anomalies sur CSV de reference ({len(collected)}): {joined}")
