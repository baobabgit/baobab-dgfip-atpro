"""Normalisation des noms d'agents.

:spec: FEAT-010.1
"""

from __future__ import annotations

from atpro.parser.normalizers.normalized_identity import NormalizedIdentity
from atpro.parser.normalizers.text_normalizer import TextNormalizer


class AgentNameNormalizer:
    """Normalise un nom d'agent sans fusion persistante.

    :spec: FEAT-010.1
    """

    def __init__(self, text_normalizer: TextNormalizer | None = None) -> None:
        """Injecte le normaliseur texte.

        :param text_normalizer: Collaborateur texte.
        """
        self._text = text_normalizer or TextNormalizer()

    def normalize(self, value: str) -> NormalizedIdentity:
        """Produit une identite agent normalisee.

        :param value: Nom brut issu du CSV.
        :returns: Identite avec indices prenom/nom et ambiguite.
        :spec: FEAT-010.1
        """
        raw = value
        compact = self._text.normalize(value)
        if compact == "":
            return NormalizedIdentity(
                raw_value=raw,
                normalized_value="",
                confidence=0.0,
                is_ambiguous=True,
                ambiguity_reasons=("empty_value",),
            )

        normalized = self._text.normalize_for_compare(compact)
        tokens = compact.split(" ")
        first_hint: str | None = None
        last_hint: str | None = None
        confidence = 0.7
        ambiguous = False
        reasons: list[str] = []

        if len(tokens) == 1:
            last_hint = tokens[0]
            confidence = 0.4
            ambiguous = True
            reasons.append("single_token")
        else:
            first_token, last_token = tokens[0], tokens[-1]
            if self._is_all_caps(first_token) and not self._is_all_caps(last_token):
                last_hint = first_token
                first_hint = " ".join(tokens[1:])
                confidence = 0.85
            elif not self._is_all_caps(first_token) and self._is_all_caps(last_token):
                first_hint = " ".join(tokens[:-1])
                last_hint = last_token
                confidence = 0.9
            else:
                first_hint = first_token
                last_hint = last_token
                ambiguous = True
                reasons.append("case_pattern_unclear")
                confidence = 0.55

            if any("-" in token for token in tokens):
                confidence = min(1.0, confidence + 0.05)

        return NormalizedIdentity(
            raw_value=raw,
            normalized_value=normalized,
            first_name_hint=first_hint,
            last_name_hint=last_hint,
            confidence=confidence,
            is_ambiguous=ambiguous,
            ambiguity_reasons=tuple(reasons),
        )

    @staticmethod
    def _is_all_caps(token: str) -> bool:
        """Indique si le jeton est en majuscules (lettres uniquement).

        :param token: Mot a tester.
        :returns: True si majuscules.
        """
        letters = [char for char in token if char.isalpha()]
        if not letters:
            return False
        return all(char.isupper() for char in letters)
