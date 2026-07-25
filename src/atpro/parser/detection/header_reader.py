"""Lecture des en-tetes CSV.

:spec: FEAT-002.2
"""

from __future__ import annotations

import csv
from io import StringIO


class HeaderReader:
    """Extrait la premiere ligne d'en-tetes.

    :spec: FEAT-002.2
    """

    def read(self, text_sample: str, separator: str) -> tuple[str, ...]:
        """Lit les colonnes brutes de la premiere ligne non vide.

        :param text_sample: Texte decode.
        :param separator: Separateur detecte.
        :returns: Tuple des cellules d'en-tete (peut etre vide).
        """
        for line in text_sample.splitlines():
            if not line.strip():
                continue
            reader = csv.reader(StringIO(line), delimiter=separator, quotechar='"')
            try:
                row = next(reader)
            except StopIteration:
                return ()
            return tuple(cell.strip() for cell in row)
        return ()
