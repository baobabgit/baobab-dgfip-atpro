"""Diagnostic structure de parsing.

:spec: FEAT-003.1
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from atpro.domain.enums.import_severity import ImportSeverity
from atpro.domain.exceptions.domain_error import DomainError


@dataclass(frozen=True, slots=True)
class ParseIssue:
    """Issue de validation ou de parsing.

    :param code: Code stable pour les tests.
    :param message: Message comprehensible.
    :param severity: Niveau de severite.
    :param row_number: Numero de ligne (nullable).
    :param column: Nom de colonne (nullable).
    :param raw_value: Valeur brute deja masquee si sensible.
    :param hint: Conseil technique optionnel.
    :spec: FEAT-003.1
    """

    code: str
    message: str
    severity: ImportSeverity
    row_number: int | None = None
    column: str | None = None
    raw_value: str | None = None
    hint: str | None = None

    def __post_init__(self) -> None:
        """Valide les champs obligatoires.

        :raises DomainError: Si code ou message est vide.
        """
        if not self.code.strip():
            raise DomainError("ParseIssue.code obligatoire")
        if not self.message.strip():
            raise DomainError("ParseIssue.message obligatoire")

    def to_dict(self) -> dict[str, Any]:
        """Serialise l'issue en dictionnaire JSON-compatible.

        :returns: Representation dictionnaire.
        """
        payload = asdict(self)
        payload["severity"] = self.severity.value
        return payload
