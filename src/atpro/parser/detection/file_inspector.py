"""Service d'inspection bas niveau des fichiers CSV.

:spec: FEAT-002.1
"""

from __future__ import annotations

from pathlib import Path

from atpro.parser.detection.encoding_detector import EncodingDetector
from atpro.parser.detection.file_detection_error import FileDetectionError
from atpro.parser.detection.file_inspection import FileInspection
from atpro.parser.detection.header_normalizer import HeaderNormalizer
from atpro.parser.detection.header_reader import HeaderReader
from atpro.parser.detection.separator_detector import SeparatorDetector
from atpro.parser.detection.sha256_streamer import Sha256Streamer
from atpro.parser.results.import_warning import ImportWarning


class FileInspector:
    """Inspecte encodage, separateur, en-tetes et SHA-256.

    Ne parse pas les enregistrements metier : un seul parcours binaire pour
    l'empreinte, puis analyse d'un echantillon pour le reste.

    :spec: FEAT-002.1
    """

    def __init__(
        self,
        *,
        streamer: Sha256Streamer | None = None,
        encoding_detector: EncodingDetector | None = None,
        separator_detector: SeparatorDetector | None = None,
        header_reader: HeaderReader | None = None,
        header_normalizer: HeaderNormalizer | None = None,
    ) -> None:
        """Injecte les collaborateurs (tests).

        :param streamer: Calculateur SHA-256.
        :param encoding_detector: Detecteur d'encodage.
        :param separator_detector: Detecteur de separateur.
        :param header_reader: Lecteur d'en-tetes.
        :param header_normalizer: Normaliseur d'en-tetes.
        """
        self._streamer = streamer or Sha256Streamer()
        self._encoding_detector = encoding_detector or EncodingDetector()
        self._separator_detector = separator_detector or SeparatorDetector()
        self._header_reader = header_reader or HeaderReader()
        self._header_normalizer = header_normalizer or HeaderNormalizer()

    def inspect(self, path: Path) -> FileInspection:
        """Produit les metadonnees d'inspection.

        :param path: Chemin du fichier CSV.
        :returns: Inspection serialisable.
        :raises FileDetectionError: Fichier absent ou vide.
        :spec: FEAT-002.1
        """
        resolved = path.expanduser()
        if not resolved.is_file():
            raise FileDetectionError(
                "FILE_ABSENT",
                f"fichier absent: {resolved}",
            )
        if resolved.stat().st_size == 0:
            raise FileDetectionError(
                "FILE_EMPTY",
                f"fichier vide: {resolved}",
            )

        digest = self._streamer.digest(resolved)
        encoding = self._encoding_detector.detect(digest.sample)
        text_sample = digest.sample.decode(encoding.encoding, errors="replace")
        separator = self._separator_detector.detect(text_sample)
        raw_columns = self._header_reader.read(text_sample, separator.separator)
        normalized = self._header_normalizer.normalize_many(raw_columns)

        warnings: list[ImportWarning] = []
        if encoding.degraded:
            warnings.append(
                ImportWarning.create(
                    code="ENC_DEGRADED",
                    message=(
                        "detection d'encodage degradee ; "
                        f"fallback {encoding.encoding}"
                    ),
                    hint="verifier le fichier source ou forcer l'encodage",
                )
            )
        if not raw_columns:
            warnings.append(
                ImportWarning.create(
                    code="HEADER_MISSING",
                    message="aucune ligne d'en-tete exploitable dans l'echantillon",
                )
            )

        return FileInspection(
            path=str(resolved),
            file_name=resolved.name,
            size_bytes=digest.size_bytes,
            sha256=digest.sha256,
            encoding=encoding.encoding,
            encoding_confidence=encoding.confidence,
            separator=separator.separator,
            separator_confidence=separator.confidence,
            raw_columns=raw_columns,
            normalized_columns=normalized,
            lines_read=digest.line_count,
            warnings=tuple(warnings),
        )
