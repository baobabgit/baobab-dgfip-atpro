"""Registre des schemas CSV connus.

:spec: FEAT-002.3
"""

from __future__ import annotations

from atpro.domain.enums.import_file_type import ImportFileType
from atpro.domain.enums.schema_version import SchemaVersion
from atpro.parser.schemas.file_schema import FileSchema


class SchemaRegistry:
    """Catalogue des signatures de fichiers AT Pro.

    :spec: FEAT-002.3
    """

    def __init__(self, schemas: tuple[FileSchema, ...] | None = None) -> None:
        """Initialise le registre.

        :param schemas: Signatures injectables (tests) ; defaut = catalogue v0.1.
        """
        self._schemas = schemas if schemas is not None else self.default_schemas()

    def all(self) -> tuple[FileSchema, ...]:
        """Retourne toutes les signatures.

        :returns: Tuple ordonne de schemas.
        """
        return self._schemas

    def get(self, schema_id: str) -> FileSchema | None:
        """Recherche un schema par identifiant.

        :param schema_id: Identifiant stable.
        :returns: Schema ou ``None``.
        """
        for schema in self._schemas:
            if schema.schema_id == schema_id:
                return schema
        return None

    @staticmethod
    def default_schemas() -> tuple[FileSchema, ...]:
        """Construit le catalogue issu du cahier des charges.

        :returns: Signatures v0.1.0.
        :spec: FEAT-002.3
        """
        return (
            FileSchema(
                schema_id="incoming_calls_v1",
                file_type=ImportFileType.INCOMING_CALLS,
                schema_version=SchemaVersion.V1,
                required_columns=frozenset(
                    {
                        "id_de_l_appel",
                        "numero_appelant",
                        "numero_appele",
                        "nom_de_l_agent",
                        "debut_d_appel",
                        "fin_d_appel",
                        "flux",
                        "service",
                        "noms_de_mesures",
                        "valeurs_de_mesures",
                    }
                ),
                filename_hints=frozenset({"appel", "entrant", "incoming"}),
            ),
            FileSchema(
                schema_id="outgoing_calls_v1",
                file_type=ImportFileType.OUTGOING_CALLS,
                schema_version=SchemaVersion.V1,
                required_columns=frozenset(
                    {
                        "id_de_l_appel",
                        "numero_appele",
                        "nom_de_l_agent",
                        "debut_d_appel",
                        "fin_d_appel",
                        "noms_de_mesures",
                        "valeurs_de_mesures",
                    }
                ),
                optional_columns=frozenset({"numero_appelant"}),
                filename_hints=frozenset({"sortant", "outgoing", "sotant"}),
            ),
            FileSchema(
                schema_id="tickets_long",
                file_type=ImportFileType.TICKETS,
                schema_version=SchemaVersion.V1,
                required_columns=frozenset(
                    {
                        "numero_ticket",
                        "date_heure_creation_ticket",
                        "statut_ticket",
                        "site_repartition_ticket",
                        "canal",
                        "priorite",
                        "agent_qualification",
                        "agent_resolution",
                        "agent_cloture",
                        "groupe",
                        "domaine",
                    }
                ),
                filename_hints=frozenset({"ticket"}),
            ),
            FileSchema(
                schema_id="tickets_reduced",
                file_type=ImportFileType.TICKETS,
                schema_version=SchemaVersion.V1,
                required_columns=frozenset(
                    {
                        "numero_ticket",
                        "date_heure_creation_ticket",
                        "statut_ticket",
                        "site_repartition_ticket",
                    }
                ),
                optional_columns=frozenset({"canal", "nature"}),
                filename_hints=frozenset({"ticket"}),
            ),
            FileSchema(
                schema_id="activities_wide",
                file_type=ImportFileType.AGENT_ACTIVITIES,
                schema_version=SchemaVersion.V1,
                required_columns=frozenset(
                    {
                        "periode",
                        "agent_groupe_agent",
                        "appels_decroches",
                        "appels_recus",
                        "temps_login",
                        "temps_pret",
                    }
                ),
                filename_hints=frozenset({"activit", "agent"}),
            ),
            FileSchema(
                schema_id="activities_long",
                file_type=ImportFileType.AGENT_ACTIVITIES,
                schema_version=SchemaVersion.V1,
                required_columns=frozenset(
                    {
                        "periode",
                        "agent_groupe_agent",
                        "noms_de_mesures",
                        "valeurs_de_mesures",
                    }
                ),
                filename_hints=frozenset({"activit", "agent"}),
            ),
        )
