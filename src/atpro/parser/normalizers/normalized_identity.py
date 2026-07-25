"""Identite normalisee sans rapprochement persistant.

:spec: FEAT-010.1
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class NormalizedIdentity:
    """Identite brute + forme normalisee et indices optionnels.

    Aucune fusion definitive n'est realisee : seuls des indices sont fournis.

    :param raw_value: Valeur source conservee.
    :param normalized_value: Forme comparable (minuscules, sans accents).
    :param first_name_hint: Prenom detecte si applicable.
    :param last_name_hint: Nom detecte si applicable.
    :param confidence: Confiance ``[0, 1]``.
    :param is_ambiguous: True si la forme est ambigue.
    :param ambiguity_reasons: Motifs d'ambiguite.
    :spec: FEAT-010.1
    """

    raw_value: str
    normalized_value: str
    first_name_hint: str | None = None
    last_name_hint: str | None = None
    confidence: float = 1.0
    is_ambiguous: bool = False
    ambiguity_reasons: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialise l'identite.

        :returns: Dictionnaire JSON-compatible.
        """
        payload = asdict(self)
        payload["ambiguity_reasons"] = list(self.ambiguity_reasons)
        return payload
