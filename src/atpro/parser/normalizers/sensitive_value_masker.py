"""Masquage des valeurs sensibles pour diagnostics et logs.

:spec: FEAT-005.3
"""

from __future__ import annotations

import re


class SensitiveValueMasker:
    """Masque emails et numeros de telephone dans les payloads.

    :spec: FEAT-005.3
    """

    _EMAIL = re.compile(r"(?i)\b([A-Z0-9._%+-]+)@([A-Z0-9.-]+\.[A-Z]{2,})\b")
    _PHONE = re.compile(r"(?:\+?\d[\d\s.\-]{6,}\d)")

    def mask(self, value: str | None) -> str | None:
        """Masque les motifs sensibles d'une chaine.

        :param value: Texte potentiellement sensible.
        :returns: Texte masque, ou ``None`` si entree ``None``.
        """
        if value is None:
            return None
        masked = self._EMAIL.sub(self._mask_email, value)
        return self._PHONE.sub(self._mask_phone, masked)

    @staticmethod
    def _mask_email(match: re.Match[str]) -> str:
        """Remplace un email par une forme reduite.

        :param match: Correspondance email.
        :returns: Email masque.
        """
        local = match.group(1)
        domain = match.group(2)
        local_mask = local[0] + "***" if local else "***"
        return f"{local_mask}@***{domain[-3:] if len(domain) >= 3 else '***'}"

    @staticmethod
    def _mask_phone(match: re.Match[str]) -> str:
        """Remplace un numero par une forme reduite.

        :param match: Correspondance telephone.
        :returns: Numero masque.
        """
        digits = re.sub(r"\D", "", match.group(0))
        if len(digits) < 4:
            return "***"
        return f"***{digits[-2:]}"
