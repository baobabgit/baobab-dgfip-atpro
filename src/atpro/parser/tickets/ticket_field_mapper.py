"""Mapping colonnes CSV → RawTicketRow.

:spec: FEAT-007.1
"""

from __future__ import annotations

from atpro.parser.detection.header_normalizer import HeaderNormalizer
from atpro.parser.tickets.raw_ticket_row import RawTicketRow


class TicketFieldMapper:
    """Mappe un dictionnaire de cellules vers ``RawTicketRow``.

    :spec: FEAT-007.1
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
    ) -> RawTicketRow:
        """Construit une ligne brute.

        :param row_number: Numero de ligne.
        :param cells: Cellules.
        :param already_normalized_keys: Si True, cles deja normalisees.
        :returns: Ligne interne.
        """
        normalized = (
            cells
            if already_normalized_keys
            else {self._headers.normalize(key): value for key, value in cells.items()}
        )
        return RawTicketRow(
            row_number=row_number,
            external_ticket_id=self._get(normalized, "numero_ticket"),
            created_at_raw=self._get(normalized, "date_heure_creation_ticket"),
            taken_at_raw=self._get(normalized, "date_heure_prise_en_charge_ticket"),
            resolved_at_raw=self._get(normalized, "date_heure_resolution_ticket"),
            closed_at_raw=self._get(normalized, "date_heure_cloture_ticket"),
            channel=self._first(
                normalized, ("type_canal_ticket", "canal", "canal_ticket")
            ),
            nature=self._first(normalized, ("nature_ticket", "nature")),
            ticket_type=self._get(normalized, "type_ticket"),
            status=self._get(normalized, "statut_ticket"),
            distribution_site=self._get(normalized, "site_repartition_ticket"),
            qualification_agent=self._agent(
                normalized,
                combined="agent_qualification",
                first="prenom_agent_qualification_ticket",
                last="nom_agent_qualification_ticket",
            ),
            qualification_site=self._get(normalized, "site_agent_qualification_ticket"),
            resolution_agent=self._agent(
                normalized,
                combined="agent_resolution",
                first="prenom_agent_resolution_ticket",
                last="nom_agent_resolution_ticket",
            ),
            resolution_site=self._get(normalized, "site_agent_resolution_ticket"),
            closure_agent=self._agent(
                normalized,
                combined="agent_cloture",
                first="prenom_agent_cloture_ticket",
                last="nom_agent_cloture_ticket",
            ),
            group=self._first(normalized, ("groupe", "niveau_groupe_resolution")),
            domain=self._first(normalized, ("domaine", "domaine_metier")),
            contact_type=self._get(normalized, "type_contact"),
            contact_identifier=self._first(
                normalized,
                ("identifiant_contact", "telephone_contact", "email_contact"),
            ),
            form_id=self._get(normalized, "numero_formulaire"),
            form_type=self._get(normalized, "type_formulaire"),
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

    def _first(self, cells: dict[str, str], keys: tuple[str, ...]) -> str | None:
        """Retourne la premiere valeur non vide.

        :param cells: Cellules.
        :param keys: Cles candidates.
        :returns: Valeur ou ``None``.
        """
        for key in keys:
            value = self._get(cells, key)
            if value is not None:
                return value
        return None

    def _agent(
        self,
        cells: dict[str, str],
        *,
        combined: str,
        first: str,
        last: str,
    ) -> str | None:
        """Fusionne colonnes agent combinees ou nom/prenom.

        :param cells: Cellules.
        :param combined: Cle agent unique.
        :param first: Prenom.
        :param last: Nom.
        :returns: Libelle agent ou ``None``.
        """
        direct = self._get(cells, combined)
        if direct is not None:
            return direct
        parts = [p for p in (self._get(cells, first), self._get(cells, last)) if p]
        if not parts:
            return None
        return " ".join(parts)
