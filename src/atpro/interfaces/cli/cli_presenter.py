"""Presentation des sorties CLI (humain / JSON).

:spec: FEAT-002.5
"""

from __future__ import annotations

import json

from atpro.parser.detection.file_inspection import FileInspection
from atpro.parser.normalizers.sensitive_value_masker import SensitiveValueMasker
from atpro.parser.results.parse_preview import ParsePreview
from atpro.parser.results.parse_result import ParseResult


class CliPresenter:
    """Formate les sorties CLI sans logique metier.

    :param masker: Masqueur de valeurs sensibles (sorties humaines).
    :spec: FEAT-002.5
    """

    def __init__(self, masker: SensitiveValueMasker | None = None) -> None:
        """Injecte le masqueur (tests).

        :param masker: Instance de masquage.
        """
        self._masker = masker or SensitiveValueMasker()

    def format_inspection(
        self,
        inspection: FileInspection,
        *,
        as_json: bool,
        verbose: bool = False,
    ) -> str:
        """Formate une inspection fichier.

        :param inspection: Resultat d'inspection.
        :param as_json: Sortie JSON si vrai.
        :param verbose: Details supplementaires.
        :returns: Texte a afficher.
        :spec: FEAT-002.5
        """
        if as_json:
            return json.dumps(inspection.to_dict(), ensure_ascii=False, sort_keys=True)
        lines = [
            f"path: {inspection.path}",
            f"file_name: {inspection.file_name}",
            f"detected_type: {inspection.detected_type.value}",
            f"schema_version: {inspection.schema_version.value}",
            f"encoding: {inspection.encoding}",
            f"separator: {inspection.separator}",
            f"size_bytes: {inspection.size_bytes}",
            f"lines_read: {inspection.lines_read}",
            f"columns: {len(inspection.raw_columns)}",
            f"warnings: {len(inspection.warnings)}",
        ]
        if verbose and inspection.warnings:
            for warning in inspection.warnings:
                lines.append(
                    self._mask(
                        f"  warning[{warning.issue.code}]: {warning.issue.message}"
                    )
                )
        if verbose and inspection.raw_columns:
            masked_cols = ", ".join(
                self._mask(col) or "" for col in inspection.raw_columns
            )
            lines.append(f"raw_columns: {masked_cols}")
        return "\n".join(lines)

    def format_parse_result(
        self,
        result: ParseResult,
        *,
        as_json: bool,
        verbose: bool = False,
    ) -> str:
        """Formate un resultat de validation / parsing.

        :param result: Resultat standardise.
        :param as_json: Sortie JSON si vrai.
        :param verbose: Details erreurs / warnings.
        :returns: Texte a afficher.
        :spec: FEAT-002.5
        """
        if as_json:
            return result.to_json()
        lines = [
            f"status: {result.summary.status.value}",
            f"detected_type: {result.detected_type.value}",
            f"schema_version: {result.schema_version.value}",
            f"records: {result.summary.record_count}",
            f"warnings: {result.summary.warning_count}",
            f"errors: {result.summary.error_count}",
            f"path: {result.file_metadata.path}",
        ]
        if verbose:
            lines.extend(self._format_issues(result))
        return "\n".join(lines)

    def format_preview(
        self,
        preview: ParsePreview,
        *,
        as_json: bool,
        verbose: bool = False,
    ) -> str:
        """Formate un apercu de parsing.

        :param preview: Apercu limite.
        :param as_json: Sortie JSON si vrai.
        :param verbose: Details supplementaires.
        :returns: Texte a afficher.
        :spec: FEAT-002.5
        """
        if as_json:
            return preview.to_json()
        lines = [
            f"path: {preview.file_metadata.path}",
            f"detected_type: {preview.file_metadata.detected_type.value}",
            f"schema_version: {preview.file_metadata.schema_version.value}",
            f"limit: {preview.limit}",
            f"preview_records: {len(preview.records)}",
            f"warnings: {len(preview.warnings)}",
            f"errors: {len(preview.errors)}",
        ]
        if verbose:
            for index, record in enumerate(preview.records, start=1):
                lines.append(
                    self._mask(f"  record[{index}]: {self._record_summary(record)}")
                )
            for error in preview.errors:
                lines.append(
                    self._mask(f"  error[{error.issue.code}]: {error.issue.message}")
                )
            for warning in preview.warnings:
                lines.append(
                    self._mask(
                        f"  warning[{warning.issue.code}]: {warning.issue.message}"
                    )
                )
        return "\n".join(lines)

    def format_detection_error(self, code: str, message: str, *, as_json: bool) -> str:
        """Formate une erreur de detection fatale.

        :param code: Code stable.
        :param message: Message.
        :param as_json: Sortie JSON si vrai.
        :returns: Texte a afficher.
        :spec: FEAT-002.5
        """
        if as_json:
            payload = {"error": {"code": code, "message": message}}
            return json.dumps(payload, ensure_ascii=False, sort_keys=True)
        return self._mask(f"error[{code}]: {message}")

    def format_technical_error(self, message: str, *, as_json: bool) -> str:
        """Formate une erreur technique inattendue.

        :param message: Message technique.
        :param as_json: Sortie JSON si vrai.
        :returns: Texte a afficher.
        :spec: FEAT-002.5
        """
        safe = self._mask(message)
        if as_json:
            payload = {"error": {"code": "TECHNICAL_ERROR", "message": safe}}
            return json.dumps(payload, ensure_ascii=False, sort_keys=True)
        return f"error[TECHNICAL_ERROR]: {safe}"

    def _format_issues(self, result: ParseResult) -> list[str]:
        """Liste les erreurs et warnings verboses.

        :param result: Resultat a detailler.
        :returns: Lignes supplementaires.
        """
        lines: list[str] = []
        for error in result.errors:
            lines.append(
                self._mask(f"  error[{error.issue.code}]: {error.issue.message}")
            )
        for warning in result.warnings:
            lines.append(
                self._mask(f"  warning[{warning.issue.code}]: {warning.issue.message}")
            )
        return lines

    def _mask(self, value: str) -> str:
        """Applique le masquage sensible.

        :param value: Texte brut.
        :returns: Texte masque.
        """
        masked = self._masker.mask(value)
        return masked if masked is not None else ""

    @staticmethod
    def _record_summary(record: object) -> str:
        """Resume court d'un enregistrement metier.

        :param record: Objet metier.
        :returns: Representation courte.
        """
        to_dict = getattr(record, "to_dict", None)
        if callable(to_dict):
            try:
                return json.dumps(to_dict(), ensure_ascii=False, sort_keys=True)
            except (TypeError, ValueError):
                return repr(record)
        return repr(record)
