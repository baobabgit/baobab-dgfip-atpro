"""Detection du type de fichier par scoring de schemas.

:spec: FEAT-002.3
"""

from __future__ import annotations

from pathlib import Path

from atpro.domain.enums.import_file_type import ImportFileType
from atpro.domain.enums.schema_version import SchemaVersion
from atpro.parser.detection.header_normalizer import HeaderNormalizer
from atpro.parser.results.import_warning import ImportWarning
from atpro.parser.schemas.file_schema import FileSchema
from atpro.parser.schemas.missing_columns_message import MissingColumnsMessage
from atpro.parser.schemas.schema_match import SchemaMatch
from atpro.parser.schemas.schema_registry import SchemaRegistry

_FILENAME_BONUS = 0.5
_REQUIRED_WEIGHT = 2.0
_OPTIONAL_WEIGHT = 0.5
_MIN_CONFIDENCE = 0.55


class SchemaDetector:
    """Detecte le schema a partir des colonnes (pas du seul nom de fichier).

    :spec: FEAT-002.3
    """

    def __init__(
        self,
        *,
        registry: SchemaRegistry | None = None,
        normalizer: HeaderNormalizer | None = None,
        missing_message: MissingColumnsMessage | None = None,
    ) -> None:
        """Injecte registre et collaborateurs.

        :param registry: Catalogue de schemas.
        :param normalizer: Normaliseur d'en-tetes.
        :param missing_message: Fabricant de messages.
        """
        self._registry = registry or SchemaRegistry()
        self._normalizer = normalizer or HeaderNormalizer()
        self._missing_message = missing_message or MissingColumnsMessage()

    def detect(
        self,
        columns: tuple[str, ...],
        *,
        file_name: str | None = None,
        already_normalized: bool = False,
    ) -> SchemaMatch:
        """Retourne le meilleur schema pour les colonnes fournies.

        :param columns: En-tetes bruts ou deja normalises.
        :param file_name: Nom de fichier (indice faible optionnel).
        :param already_normalized: Si True, ne renormalise pas.
        :returns: Match (``unknown`` si confiance insuffisante).
        :spec: FEAT-002.3
        """
        normalized = (
            columns if already_normalized else self._normalizer.normalize_many(columns)
        )
        present = frozenset(normalized)
        scored: list[tuple[float, float, FileSchema, SchemaMatch]] = []

        for schema in self._registry.all():
            match = self._score_schema(schema, present, file_name=file_name)
            scored.append((match.score, match.confidence, schema, match))

        if not scored:
            return self._unknown(present)

        scored.sort(key=lambda item: (item[0], item[1]), reverse=True)
        _best_score, best_confidence, best_schema, best_match = scored[0]

        # Completude stricte : toutes les colonnes requises presentes.
        if best_match.missing_required:
            # Si le meilleur a des manques, tenter le second s'il est complet.
            for _score, confidence, schema, match in scored[1:]:
                if not match.missing_required and confidence >= _MIN_CONFIDENCE:
                    return self._with_extra_warning(match, present, schema)
            return self._unknown(
                present,
                candidate=best_schema,
                missing=best_match.missing_required,
            )

        if best_confidence < _MIN_CONFIDENCE:
            return self._unknown(present, candidate=best_schema)

        return self._with_extra_warning(best_match, present, best_schema)

    def _score_schema(
        self,
        schema: FileSchema,
        present: frozenset[str],
        *,
        file_name: str | None,
    ) -> SchemaMatch:
        """Calcule le score d'une signature.

        :param schema: Signature candidate.
        :param present: Colonnes normalisees presentes.
        :param file_name: Nom de fichier optionnel.
        :returns: Match partiel pour ce schema.
        """
        matched_required = tuple(
            sorted(col for col in schema.required_columns if col in present)
        )
        missing_required = tuple(
            sorted(col for col in schema.required_columns if col not in present)
        )
        matched_optional = tuple(
            sorted(col for col in schema.optional_columns if col in present)
        )
        known = schema.required_columns | schema.optional_columns
        extra_columns = tuple(sorted(col for col in present if col not in known))

        score = (
            len(matched_required) * _REQUIRED_WEIGHT
            + len(matched_optional) * _OPTIONAL_WEIGHT
            - len(missing_required) * _REQUIRED_WEIGHT
        )
        if file_name and self._filename_hint_matches(file_name, schema):
            score += _FILENAME_BONUS

        required_total = len(schema.required_columns)
        coverage = len(matched_required) / required_total
        confidence = coverage
        if missing_required:
            confidence *= 0.5
        if file_name and self._filename_hint_matches(file_name, schema):
            confidence = min(1.0, confidence + 0.05)

        warnings: list[ImportWarning] = []
        missing_warning = self._missing_message.build(
            schema_id=schema.schema_id,
            missing_required=missing_required,
        )
        if missing_warning is not None:
            warnings.append(missing_warning)

        return SchemaMatch(
            schema_id=schema.schema_id,
            file_type=schema.file_type,
            schema_version=schema.schema_version,
            score=score,
            confidence=confidence,
            matched_required=matched_required,
            missing_required=missing_required,
            extra_columns=extra_columns,
            warnings=tuple(warnings),
        )

    @staticmethod
    def _filename_hint_matches(file_name: str, schema: FileSchema) -> bool:
        """Indique si le nom contient un indice du schema.

        :param file_name: Nom de fichier.
        :param schema: Signature.
        :returns: True si un hint matche.
        """
        lowered = Path(file_name).name.lower()
        return any(hint in lowered for hint in schema.filename_hints)

    def _with_extra_warning(
        self,
        match: SchemaMatch,
        present: frozenset[str],
        schema: FileSchema,
    ) -> SchemaMatch:
        """Ajoute un warning pour colonnes supplementaires.

        :param match: Match retenu.
        :param present: Colonnes presentes.
        :param schema: Schema retenu.
        :returns: Match éventuellement enrichi.
        """
        if not match.extra_columns:
            return match
        warning = ImportWarning.create(
            code="SCHEMA_EXTRA_COLUMNS",
            message=(
                "colonnes supplementaires ignorees pour "
                f"{schema.schema_id}: {', '.join(match.extra_columns)}"
            ),
        )
        return SchemaMatch(
            schema_id=match.schema_id,
            file_type=match.file_type,
            schema_version=match.schema_version,
            score=match.score,
            confidence=match.confidence,
            matched_required=match.matched_required,
            missing_required=match.missing_required,
            extra_columns=match.extra_columns,
            warnings=(*match.warnings, warning),
        )

    def _unknown(
        self,
        present: frozenset[str],
        *,
        candidate: FileSchema | None = None,
        missing: tuple[str, ...] = (),
    ) -> SchemaMatch:
        """Construit un resultat inconnu.

        :param present: Colonnes observees.
        :param candidate: Meilleur candidat refuse.
        :param missing: Colonnes manquantes du candidat.
        :returns: Match ``unknown``.
        """
        warnings: list[ImportWarning] = [
            ImportWarning.create(
                code="SCHEMA_UNKNOWN",
                message="aucune signature de schema n'atteint le seuil de confiance",
            )
        ]
        if candidate is not None and missing:
            built = self._missing_message.build(
                schema_id=candidate.schema_id,
                missing_required=missing,
            )
            if built is not None:
                warnings.append(built)
        return SchemaMatch(
            schema_id="unknown",
            file_type=ImportFileType.UNKNOWN,
            schema_version=SchemaVersion.UNKNOWN,
            score=0.0,
            confidence=0.0,
            matched_required=(),
            missing_required=missing,
            extra_columns=tuple(sorted(present)),
            warnings=tuple(warnings),
        )
