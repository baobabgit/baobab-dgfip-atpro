"""Normalisation des noms de sites.

:spec: FEAT-010.1
"""

from __future__ import annotations

from atpro.parser.normalizers.normalized_identity import NormalizedIdentity
from atpro.parser.normalizers.text_normalizer import TextNormalizer


class SiteNameNormalizer:
    """Normalise un libelle de site sans invention.

    :spec: FEAT-010.1
    """

    def __init__(self, text_normalizer: TextNormalizer | None = None) -> None:
        """Injecte le normaliseur texte.

        :param text_normalizer: Collaborateur texte.
        """
        self._text = text_normalizer or TextNormalizer()

    def normalize(self, value: str) -> NormalizedIdentity:
        """Produit une identite site.

        Ne cree jamais de site absent : une valeur vide reste vide.

        :param value: Libelle brut.
        :returns: Identite site (sans prenom/nom).
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
        return NormalizedIdentity(
            raw_value=raw,
            normalized_value=self._text.normalize_for_compare(compact),
            confidence=1.0,
            is_ambiguous=False,
        )
