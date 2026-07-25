"""Hachage des numeros de telephone pour les modeles.

:spec: FEAT-005.4
"""

from __future__ import annotations

import hashlib


class PhoneHasher:
    """Produit une empreinte SHA-256 des numeros (pas de clair).

    :spec: FEAT-005.4
    """

    def hash(self, value: str | None) -> str | None:
        """Hache un numero.

        :param value: Numero brut.
        :returns: Digest hex, ou ``None`` si vide.
        """
        if value is None:
            return None
        text = value.strip()
        if text == "":
            return None
        return hashlib.sha256(text.encode("utf-8")).hexdigest()
