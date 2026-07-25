# Contrat parseur CSV v0.1.0

Package : `atpro.parser`  
Références : FEAT-002.1 à FEAT-002.4, FEAT-003.1, FEAT-005.3, FEAT-005.4,
FEAT-006.1 à FEAT-010.1

## Entrées

- chemin de fichier CSV ;
- encodage détecté (ou forcé via collaborateur injecté) ;
- séparateur détecté ;
- option de limite pour `preview`.

## Sorties

| Type | Module | Usage |
|---|---|---|
| `FileInspection` | `atpro.parser.detection` | Inspection |
| `ParseResult` | `atpro.parser.results` | Validation / parsing |
| `ParsePreview` | `atpro.parser.results` | Aperçu borné |

## Orchestrateur

Point d'entrée unique : `atpro.parser.ParseFileUseCase`.

Flux :

1. `FileInspector` — encodage, séparateur, en-têtes, SHA-256, digest ;
2. `SchemaDetector` + `SchemaRegistry` — type et schéma ;
3. reader métier selon le schéma ;
4. assemblage `ParseResult` / `ParsePreview` (erreurs et warnings structurés).

## Readers

| Classe | Schéma(s) | Module |
|---|---|---|
| `IncomingCallsReader` | `incoming_calls_v1` | `atpro.parser.readers` |
| `OutgoingCallsReader` | `outgoing_calls_v1` | `atpro.parser.readers` |
| `TicketsReader` | `tickets_long`, `tickets_reduced` | `atpro.parser.readers` |
| `AgentActivitiesWideReader` | `activities_wide` | `atpro.parser.readers` |
| `AgentActivitiesLongReader` | `activities_long` | `atpro.parser.readers` |

## Schémas reconnus (v0.1.0)

Catalogue : `SchemaRegistry.default_schemas()` (`atpro.parser.schemas`).

| `schema_id` | Type fichier | Variante |
|---|---|---|
| `incoming_calls_v1` | appels entrants | colonnes mesures / valeurs |
| `outgoing_calls_v1` | appels sortants | `numero_appelant` optionnel |
| `tickets_long` | tickets | jeu long (agents, domaine, etc.) |
| `tickets_reduced` | tickets | jeu réduit |
| `activities_wide` | activités agents | colonnes métriques larges |
| `activities_long` | activités agents | mesures / valeurs (format long) |

Règles :

- détection par **colonnes et contenu**, pas uniquement par nom de fichier ;
- indices de nom de fichier (`filename_hints`) sont secondaires ;
- colonnes normalisées (accents, casse) avant matching.

Colonnes obligatoires détaillées dans le code
`src/atpro/parser/schemas/schema_registry.py` (source de vérité exécutable).

## Normalizers

Sous-package `atpro.parser.normalizers` :

| Classe | Rôle |
|---|---|
| `DateNormalizer` | Dates → `datetime` aware `Europe/Paris` (formats FR courants) |
| `DurationNormalizer` | Secondes entières ou `HH:MM:SS` → `DurationSeconds` |
| `PercentageNormalizer` | Pourcentages à virgule (`100,00%`, `12,5`) → `Percentage` |
| `TextNormalizer` | Nettoyage / comparaison de libellés |
| `AgentNameNormalizer` | Identité agent (`NormalizedIdentity`), sans fusion persistante |
| `SiteNameNormalizer` | Identité site, sans invention de site absent |
| `SensitiveValueMasker` | Masquage emails / téléphones dans diagnostics et sorties |
| `NormalizationError` | Erreur de normalisation (code + valeur brute) |

## Comportements obligatoires

- consolidation des appels multi-lignes ;
- conservation de la provenance ligne ;
- erreurs et avertissements structurés (`ParseIssue`, `ImportError`, `ImportWarning`) ;
- masquage des données sensibles dans les diagnostics ;
- **pas d'accès base de données**.

## Validation de référence

- Fixtures anonymisées sous `tests/fixtures/csv/` — obligatoires en CI.
- Suite de non-régression : `tests/unit/atpro/regression/`.
- CSV réels optionnels, cadrés par `docs/reference-data.md` (hors dépôt si volumineux).

## Limites v0.1.0 (parseur)

- Pas de persistence des résultats.
- Pas d'API HTTP.
- Pas de calcul statistique ni de rapports.
- Pas de rapprochement agent irréversible (normalisation seulement).
