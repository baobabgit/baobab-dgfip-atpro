"""Normalisation de texte generique.

:spec: FEAT-005.3
"""

from __future__ import annotations

import re
import unicodedata


class TextNormalizer:
    """Normalise les chaines issues des CSV.

    :spec: FEAT-005.3
    """

    _MULTI_SPACE = re.compile(r"\s+")

    def normalize(self, value: str) -> str:
        """Supprime les espaces en trop sans changer la casse.

        :param value: Texte brut.
        :returns: Texte compacte.
        """
        return self._MULTI_SPACE.sub(" ", value.strip())

    def normalize_for_compare(self, value: str) -> str:
        """Produit une forme comparable (minuscules, sans accents).

        :param value: Texte brut.
        :returns: Cle de comparaison.
        """
        compact = self.normalize(value).lower()
        decomposed = unicodedata.normalize("NFKD", compact)
        return "".join(char for char in decomposed if not unicodedata.combining(char))
