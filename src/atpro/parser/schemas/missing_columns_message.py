"""Messages diagnostiques pour colonnes manquantes.

:spec: FEAT-002.3
"""

from __future__ import annotations

from atpro.parser.results.import_warning import ImportWarning


class MissingColumnsMessage:
    """Construit les messages de colonnes obligatoires absentes.

    :spec: FEAT-002.3
    """

    def build(
        self,
        *,
        schema_id: str,
        missing_required: tuple[str, ...],
    ) -> ImportWarning | None:
        """Cree un warning si des colonnes manquent.

        :param schema_id: Schema evalue.
        :param missing_required: Colonnes normalisees absentes.
        :returns: Warning ou ``None``.
        """
        if not missing_required:
            return None
        listed = ", ".join(missing_required)
        return ImportWarning.create(
            code="SCHEMA_MISSING_COLUMNS",
            message=(
                f"colonnes obligatoires absentes pour le schema "
                f"{schema_id}: {listed}"
            ),
            hint="verifier l'export source ou la variante de schema",
        )
