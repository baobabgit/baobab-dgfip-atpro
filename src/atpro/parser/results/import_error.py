"""Erreur d'import structuree.

:spec: FEAT-003.1
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from atpro.domain.enums.import_severity import ImportSeverity
from atpro.domain.exceptions.domain_error import DomainError
from atpro.parser.results.parse_issue import ParseIssue


@dataclass(frozen=True, slots=True)
class ImportError:
    """Erreur structuree lors d'un import (non exception Python).

    :param issue: Diagnostic sous-jacent (severity ERROR ou FATAL).
    :spec: FEAT-003.1
    """

    issue: ParseIssue

    def __post_init__(self) -> None:
        """Verifie que la severite est bloquante.

        :raises DomainError: Si la severite n'est pas ERROR/FATAL.
        """
        if self.issue.severity not in {ImportSeverity.ERROR, ImportSeverity.FATAL}:
            raise DomainError("ImportError exige une severite error ou fatal")

    @classmethod
    def create(
        cls,
        *,
        code: str,
        message: str,
        row_number: int | None = None,
        column: str | None = None,
        raw_value: str | None = None,
        hint: str | None = None,
        severity: ImportSeverity = ImportSeverity.ERROR,
    ) -> ImportError:
        """Factory d'erreur.

        :returns: Instance valide.
        """
        return cls(
            issue=ParseIssue(
                code=code,
                message=message,
                severity=severity,
                row_number=row_number,
                column=column,
                raw_value=raw_value,
                hint=hint,
            )
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialise l'erreur.

        :returns: Dictionnaire JSON-compatible.
        """
        return {"issue": self.issue.to_dict()}
