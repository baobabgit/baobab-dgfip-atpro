"""Mapping colonnes normalisees → RawCallRow.

:spec: FEAT-005.4
"""

from __future__ import annotations

from atpro.parser.calls.raw_call_row import RawCallRow
from atpro.parser.detection.header_normalizer import HeaderNormalizer


class CallFieldMapper:
    """Mappe un dictionnaire de cellules vers ``RawCallRow``.

    :spec: FEAT-005.4
    """

    def __init__(self, header_normalizer: HeaderNormalizer | None = None) -> None:
        """Injecte le normaliseur d'en-tetes.

        :param header_normalizer: Collaborateur.
        """
        self._headers = header_normalizer or HeaderNormalizer()

    def map_row(
        self,
        row_number: int,
        cells: dict[str, str],
        *,
        already_normalized_keys: bool = False,
    ) -> RawCallRow:
        """Construit une ligne brute.

        :param row_number: Numero de ligne.
        :param cells: Cellules (cles brutes ou normalisees).
        :param already_normalized_keys: Si True, ne renormalise pas les cles.
        :returns: Ligne interne.
        """
        normalized = (
            cells
            if already_normalized_keys
            else {self._headers.normalize(key): value for key, value in cells.items()}
        )
        return RawCallRow(
            row_number=row_number,
            external_call_id=self._get(normalized, "id_de_l_appel"),
            caller=self._get(normalized, "numero_appelant"),
            callee=self._get(normalized, "numero_appele"),
            agent_name=self._get(normalized, "nom_de_l_agent"),
            started_at_raw=self._get(normalized, "debut_d_appel"),
            ended_at_raw=self._get(normalized, "fin_d_appel"),
            flow=self._get(normalized, "flux"),
            service=self._get(normalized, "service"),
            measure_name=self._get(normalized, "noms_de_mesures"),
            measure_value=self._get(normalized, "valeurs_de_mesures"),
            qualification_category=self._get(normalized, "categorie_de_qualification"),
            qualification_reason=self._get(normalized, "motif_de_qualification"),
            hangup_origin=self._get(normalized, "origine_du_raccroche"),
        )

    @staticmethod
    def _get(cells: dict[str, str], key: str) -> str | None:
        """Lit une cellule optionnelle.

        :param cells: Dictionnaire normalise.
        :param key: Cle.
        :returns: Valeur ou ``None``.
        """
        value = cells.get(key)
        if value is None:
            return None
        text = value.strip()
        return text if text else None
