"""Codes de sortie CLI.

:spec: FEAT-002.5
"""

from __future__ import annotations

from enum import IntEnum

from atpro.domain.enums.import_severity import ImportSeverity
from atpro.domain.enums.parse_status import ParseStatus
from atpro.parser.results.parse_preview import ParsePreview
from atpro.parser.results.parse_result import ParseResult


class ExitCode(IntEnum):
    """Codes de sortie stables du CLI ``atpro``.

    :spec: FEAT-002.5
    """

    SUCCESS = 0
    INVALID_FILE = 1
    MISSING_OR_UNREADABLE = 2
    UNKNOWN_FORMAT = 3
    TECHNICAL_ERROR = 4

    @classmethod
    def from_parse_result(cls, result: ParseResult) -> ExitCode:
        """Derive le code de sortie d'un ``ParseResult``.

        :param result: Resultat de validation / parsing.
        :returns: Code de sortie FEAT-002.5.
        :spec: FEAT-002.5
        """
        error_codes = {error.issue.code for error in result.errors}
        if "FILE_TYPE_UNKNOWN" in error_codes:
            return cls.UNKNOWN_FORMAT
        if any(error.issue.severity is ImportSeverity.FATAL for error in result.errors):
            return cls.MISSING_OR_UNREADABLE
        if result.errors or result.summary.status is ParseStatus.FAILED:
            return cls.INVALID_FILE
        return cls.SUCCESS

    @classmethod
    def from_parse_preview(cls, preview: ParsePreview) -> ExitCode:
        """Derive le code de sortie d'un ``ParsePreview``.

        :param preview: Apercu de parsing.
        :returns: Code de sortie FEAT-002.5.
        :spec: FEAT-002.5
        """
        synthetic = ParseResult.build(
            file_metadata=preview.file_metadata,
            records=preview.records,
            warnings=preview.warnings,
            errors=preview.errors,
        )
        return cls.from_parse_result(synthetic)
