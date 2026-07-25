"""Normalisation des en-tetes CSV.

:spec: FEAT-002.2
"""

from __future__ import annotations

import re
import unicodedata


class HeaderNormalizer:
    """Normalise les en-tetes pour comparaison stable.

    :spec: FEAT-002.2
    """

    _NON_ALNUM = re.compile(r"[^a-z0-9]+")

    def normalize(self, header: str) -> str:
        """Normalise un en-tete brut.

        :param header: Libelle source.
        :returns: Forme comparable (minuscules, sans accents).
        """
        stripped = header.strip().lower()
        decomposed = unicodedata.normalize("NFKD", stripped)
        without_marks = "".join(
            char for char in decomposed if not unicodedata.combining(char)
        )
        collapsed = self._NON_ALNUM.sub("_", without_marks)
        return collapsed.strip("_")

    def normalize_many(self, headers: tuple[str, ...]) -> tuple[str, ...]:
        """Normalise une sequence d'en-tetes.

        :param headers: En-tetes bruts.
        :returns: Tuple normalise.
        """
        return tuple(self.normalize(item) for item in headers)
