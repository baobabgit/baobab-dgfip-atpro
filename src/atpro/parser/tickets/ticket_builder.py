"""Construction de Ticket depuis RawTicketRow.

:spec: FEAT-007.1
"""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime

from atpro.domain.enums.import_severity import ImportSeverity
from atpro.domain.tickets.ticket import Ticket
from atpro.parser.calls.phone_hasher import PhoneHasher
from atpro.parser.normalizers.agent_name_normalizer import AgentNameNormalizer
from atpro.parser.normalizers.date_normalizer import DateNormalizer
from atpro.parser.normalizers.normalization_error import NormalizationError
from atpro.parser.normalizers.normalized_identity import NormalizedIdentity
from atpro.parser.normalizers.sensitive_value_masker import SensitiveValueMasker
from atpro.parser.normalizers.site_name_normalizer import SiteNameNormalizer
from atpro.parser.normalizers.text_normalizer import TextNormalizer
from atpro.parser.results.import_error import ImportError
from atpro.parser.results.import_warning import ImportWarning
from atpro.parser.tickets.raw_ticket_row import RawTicketRow
from atpro.parser.tickets.ticket_import_result import TicketImportResult


class TicketBuilder:
    """Transforme des lignes brutes en ``Ticket`` et diagnostics.

    :spec: FEAT-007.1
    """

    def __init__(
        self,
        *,
        dates: DateNormalizer | None = None,
        texts: TextNormalizer | None = None,
        agents: AgentNameNormalizer | None = None,
        sites: SiteNameNormalizer | None = None,
        phones: PhoneHasher | None = None,
        masker: SensitiveValueMasker | None = None,
        source_system: str = "csv",
    ) -> None:
        """Injecte les collaborateurs.

        :param dates: Normaliseur de dates.
        :param texts: Normaliseur de texte.
        :param agents: Normaliseur agents.
        :param sites: Normaliseur sites.
        :param phones: Hacheur contacts.
        :param masker: Masqueur diagnostics.
        :param source_system: Systeme source par defaut.
        """
        self._dates = dates or DateNormalizer()
        self._texts = texts or TextNormalizer()
        self._agents = agents or AgentNameNormalizer(self._texts)
        self._sites = sites or SiteNameNormalizer(self._texts)
        self._phones = phones or PhoneHasher()
        self._masker = masker or SensitiveValueMasker()
        self._source_system = source_system

    def build(self, rows: list[RawTicketRow]) -> TicketImportResult:
        """Construit les tickets.

        :param rows: Lignes mappees.
        :returns: Resultat d'import.
        """
        tickets: list[Ticket] = []
        agents: list[NormalizedIdentity] = []
        sites: list[NormalizedIdentity] = []
        errors: list[ImportError] = []
        warnings: list[ImportWarning] = []
        now = datetime.now(UTC)

        for row in rows:
            ticket, row_agents, row_sites, row_errors, row_warnings = self._build_one(
                row, now
            )
            errors.extend(row_errors)
            warnings.extend(row_warnings)
            agents.extend(row_agents)
            sites.extend(row_sites)
            if ticket is not None:
                tickets.append(ticket)

        return TicketImportResult(
            tickets=tuple(tickets),
            agent_identities=tuple(agents),
            site_identities=tuple(sites),
            errors=tuple(errors),
            warnings=tuple(warnings),
        )

    def _build_one(self, row: RawTicketRow, now: datetime) -> tuple[
        Ticket | None,
        list[NormalizedIdentity],
        list[NormalizedIdentity],
        list[ImportError],
        list[ImportWarning],
    ]:
        """Traite une ligne.

        :param row: Ligne brute.
        :param now: Horodatage import.
        :returns: Ticket optionnel et diagnostics.
        """
        errors: list[ImportError] = []
        warnings: list[ImportWarning] = []
        agents: list[NormalizedIdentity] = []
        sites: list[NormalizedIdentity] = []

        if row.external_ticket_id is None:
            errors.append(
                ImportError.create(
                    code="TICKET_ID_REQUIRED",
                    message="numero ticket absent",
                    row_number=row.row_number,
                    column="numero_ticket",
                )
            )
            return None, agents, sites, errors, warnings

        created_at, created_err = self._parse_date(
            row.created_at_raw,
            row_number=row.row_number,
            column="date_heure_creation_ticket",
        )
        if created_err is not None:
            errors.append(created_err)
        if created_at is None and created_err is None:
            errors.append(
                ImportError.create(
                    code="TICKET_CREATED_AT_REQUIRED",
                    message="date de creation absente",
                    row_number=row.row_number,
                    column="date_heure_creation_ticket",
                    severity=ImportSeverity.ERROR,
                )
            )
        if created_at is None:
            return None, agents, sites, errors, warnings

        taken_at, taken_err = self._parse_date(
            row.taken_at_raw,
            row_number=row.row_number,
            column="date_heure_prise_en_charge_ticket",
        )
        if taken_err is not None:
            errors.append(taken_err)

        resolved_at, resolved_err = self._parse_date(
            row.resolved_at_raw,
            row_number=row.row_number,
            column="date_heure_resolution_ticket",
        )
        if resolved_err is not None:
            errors.append(resolved_err)

        closed_at, closed_err = self._parse_date(
            row.closed_at_raw,
            row_number=row.row_number,
            column="date_heure_cloture_ticket",
        )
        if closed_err is not None:
            errors.append(closed_err)

        if resolved_at is not None and resolved_at < created_at:
            errors.append(
                ImportError.create(
                    code="TICKET_RESOLVED_BEFORE_CREATED",
                    message="resolution anterieure a la creation",
                    row_number=row.row_number,
                    column="date_heure_resolution_ticket",
                    raw_value=self._masker.mask(row.resolved_at_raw),
                )
            )
            return None, agents, sites, errors, warnings

        if closed_at is not None and closed_at < created_at:
            errors.append(
                ImportError.create(
                    code="TICKET_CLOSED_BEFORE_CREATED",
                    message="cloture anterieure a la creation",
                    row_number=row.row_number,
                    column="date_heure_cloture_ticket",
                    raw_value=self._masker.mask(row.closed_at_raw),
                )
            )
            return None, agents, sites, errors, warnings

        site_id, site_identity = self._normalize_site(
            row.distribution_site,
            row_number=row.row_number,
            column="site_repartition_ticket",
            warnings=warnings,
            required_warn=True,
        )
        if site_identity is not None:
            sites.append(site_identity)

        qual_agent_id, qual_agent = self._normalize_agent(
            row.qualification_agent,
            row_number=row.row_number,
            column="agent_qualification",
            warnings=warnings,
        )
        if qual_agent is not None:
            agents.append(qual_agent)

        qual_site_id, qual_site = self._normalize_site(
            row.qualification_site,
            row_number=row.row_number,
            column="site_agent_qualification_ticket",
            warnings=warnings,
            required_warn=False,
        )
        if qual_site is not None:
            sites.append(qual_site)

        res_agent_id, res_agent = self._normalize_agent(
            row.resolution_agent,
            row_number=row.row_number,
            column="agent_resolution",
            warnings=warnings,
        )
        if res_agent is not None:
            agents.append(res_agent)

        res_site_id, res_site = self._normalize_site(
            row.resolution_site,
            row_number=row.row_number,
            column="site_agent_resolution_ticket",
            warnings=warnings,
            required_warn=False,
        )
        if res_site is not None:
            sites.append(res_site)

        closure_agent_id, closure_agent = self._normalize_agent(
            row.closure_agent,
            row_number=row.row_number,
            column="agent_cloture",
            warnings=warnings,
        )
        if closure_agent is not None:
            agents.append(closure_agent)

        contact_hash = self._hash_contact(row.contact_identifier)
        ticket_id = self._stable_id("ticket", row.external_ticket_id)

        ticket = Ticket(
            id=ticket_id,
            source_system=self._source_system,
            external_ticket_id=row.external_ticket_id,
            form_id=row.form_id,
            form_type=row.form_type,
            created_at=created_at,
            taken_at=taken_at,
            resolved_at=resolved_at,
            closed_at=closed_at,
            channel=self._normalize_label(row.channel),
            nature=self._normalize_label(row.nature),
            ticket_type=self._normalize_label(row.ticket_type),
            status=self._normalize_label(row.status),
            contact_type=self._normalize_label(row.contact_type),
            contact_identifier_hash=contact_hash,
            creation_domain=None,
            distribution_site_id=site_id,
            resolution_group_level=self._normalize_label(row.group),
            business_domain=self._normalize_label(row.domain),
            owner_agent_id=None,
            qualification_agent_id=qual_agent_id,
            qualification_site_id=qual_site_id,
            resolution_agent_id=res_agent_id,
            resolution_site_id=res_site_id,
            closure_agent_id=closure_agent_id,
            source_import_batch_id=None,
            line_fingerprint=self._stable_id(
                "line", row.external_ticket_id, str(row.row_number)
            ),
            created_at_db=now,
            updated_at_db=now,
        )
        return ticket, agents, sites, errors, warnings

    def _parse_date(
        self,
        value: str | None,
        *,
        row_number: int,
        column: str,
    ) -> tuple[datetime | None, ImportError | None]:
        """Parse une date optionnelle.

        :param value: Valeur brute.
        :param row_number: Ligne.
        :param column: Colonne.
        :returns: Datetime et erreur optionnelle.
        """
        if value is None:
            return None, None
        try:
            return self._dates.parse(value, column=column), None
        except NormalizationError as exc:
            return None, ImportError.create(
                code="TICKET_DATE_INVALID",
                message=str(exc),
                row_number=row_number,
                column=column,
                raw_value=self._masker.mask(value),
            )

    def _normalize_label(self, value: str | None) -> str | None:
        """Normalise un libelle metier.

        :param value: Texte brut.
        :returns: Forme comparable ou ``None``.
        """
        if value is None:
            return None
        normalized = self._texts.normalize_for_compare(value)
        return normalized if normalized else None

    def _normalize_agent(
        self,
        value: str | None,
        *,
        row_number: int,
        column: str,
        warnings: list[ImportWarning],
    ) -> tuple[str | None, NormalizedIdentity | None]:
        """Normalise un agent.

        :param value: Nom brut.
        :param row_number: Ligne.
        :param column: Colonne.
        :param warnings: Accumulateur.
        :returns: Identifiant stable et identite.
        """
        if value is None:
            warnings.append(
                ImportWarning.create(
                    code="TICKET_AGENT_MISSING",
                    message=f"agent absent ({column})",
                    row_number=row_number,
                    column=column,
                )
            )
            return None, None
        identity = self._agents.normalize(value)
        if identity.normalized_value == "":
            warnings.append(
                ImportWarning.create(
                    code="TICKET_AGENT_MISSING",
                    message=f"agent vide ({column})",
                    row_number=row_number,
                    column=column,
                )
            )
            return None, identity
        return f"agent:{identity.normalized_value}", identity

    def _normalize_site(
        self,
        value: str | None,
        *,
        row_number: int,
        column: str,
        warnings: list[ImportWarning],
        required_warn: bool,
    ) -> tuple[str | None, NormalizedIdentity | None]:
        """Normalise un site.

        :param value: Libelle brut.
        :param row_number: Ligne.
        :param column: Colonne.
        :param warnings: Accumulateur.
        :param required_warn: Emmettre un warning si absent.
        :returns: Identifiant stable et identite.
        """
        if value is None:
            if required_warn:
                warnings.append(
                    ImportWarning.create(
                        code="TICKET_SITE_MISSING",
                        message=f"site absent ({column})",
                        row_number=row_number,
                        column=column,
                    )
                )
            return None, None
        identity = self._sites.normalize(value)
        if identity.normalized_value == "":
            if required_warn:
                warnings.append(
                    ImportWarning.create(
                        code="TICKET_SITE_MISSING",
                        message=f"site vide ({column})",
                        row_number=row_number,
                        column=column,
                    )
                )
            return None, identity
        return f"site:{identity.normalized_value}", identity

    def _hash_contact(self, value: str | None) -> str | None:
        """Hache un contact (telephone ou email).

        :param value: Contact brut.
        :returns: Digest hex ou ``None``.
        """
        if value is None:
            return None
        if "@" in value:
            text = value.strip().lower()
            if text == "":
                return None
            return hashlib.sha256(text.encode("utf-8")).hexdigest()
        return self._phones.hash(value)

    @staticmethod
    def _stable_id(prefix: str, *parts: str) -> str:
        """Identifiant deterministe.

        :param prefix: Prefixe.
        :param parts: Parties.
        :returns: Identifiant.
        """
        digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:16]
        return f"{prefix}-{digest}"
