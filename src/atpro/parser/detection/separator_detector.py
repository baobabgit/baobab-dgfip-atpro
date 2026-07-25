"""Detection du separateur CSV.

:spec: FEAT-002.2
"""

from __future__ import annotations

from atpro.parser.detection.separator_detection import SeparatorDetection

_CANDIDATES: tuple[str, ...] = (";", ",", "\t")
_MAX_LINES = 20


class SeparatorDetector:
    """Detecte ``;`` (prioritaire), ``,`` ou tabulation.

    :spec: FEAT-002.2
    """

    def detect(self, text_sample: str) -> SeparatorDetection:
        """Score les separateurs sur les premieres lignes.

        :param text_sample: Texte decode (echantillon).
        :returns: Separateur retenu et confiance.
        """
        lines = [line for line in text_sample.splitlines() if line.strip()][:_MAX_LINES]
        if not lines:
            return SeparatorDetection(separator=";", confidence=0.2)

        best_separator = ";"
        best_score = -1.0
        best_confidence = 0.2

        for candidate in _CANDIDATES:
            score, confidence = self._score(lines, candidate)
            # Preferer ``;`` a score egal (contrainte metier).
            if score > best_score or (score == best_score and candidate == ";"):
                best_score = score
                best_separator = candidate
                best_confidence = confidence

        return SeparatorDetection(
            separator=best_separator,
            confidence=best_confidence,
        )

    @staticmethod
    def _score(lines: list[str], separator: str) -> tuple[float, float]:
        """Evalue la coherence du nombre de champs.

        :param lines: Lignes non vides.
        :param separator: Candidat.
        :returns: Couple (score, confiance).
        """
        counts = [line.count(separator) for line in lines]
        if not counts or max(counts) == 0:
            return 0.0, 0.2

        mode = max(set(counts), key=counts.count)
        consistency = counts.count(mode) / len(counts)
        score = float(mode) * consistency
        confidence = min(1.0, 0.4 + consistency * 0.6)
        if separator == ";" and mode > 0:
            confidence = min(1.0, confidence + 0.05)
        return score, confidence
