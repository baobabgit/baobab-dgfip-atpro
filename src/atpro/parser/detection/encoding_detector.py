"""Detection d'encodage sur echantillon binaire.

:spec: FEAT-002.2
"""

from __future__ import annotations

from atpro.parser.detection.encoding_detection import EncodingDetection

_UTF8_BOM = b"\xef\xbb\xbf"


class EncodingDetector:
    """Detecte UTF-8 (avec/sans BOM) ou Windows-1252.

    :spec: FEAT-002.2
    """

    def detect(self, sample: bytes) -> EncodingDetection:
        """Inspecte un echantillon suffisant.

        :param sample: Octets en tete de fichier.
        :returns: Encodage et confiance.
        """
        if sample.startswith(_UTF8_BOM):
            return EncodingDetection(
                encoding="utf-8-sig",
                confidence=1.0,
            )

        if self._decodes(sample, "utf-8"):
            return EncodingDetection(encoding="utf-8", confidence=1.0)

        if self._decodes(sample, "cp1252"):
            return EncodingDetection(
                encoding="windows-1252",
                confidence=0.85,
            )

        # latin-1 couvre tout octet ; on signale une detection degradee.
        return EncodingDetection(
            encoding="windows-1252",
            confidence=0.35,
            degraded=True,
        )

    @staticmethod
    def _decodes(sample: bytes, encoding: str) -> bool:
        """Tente un decodage strict.

        :param sample: Octets a tester.
        :param encoding: Codec Python.
        :returns: True si le decodage reussit.
        """
        try:
            sample.decode(encoding)
        except UnicodeDecodeError:
            return False
        return True
