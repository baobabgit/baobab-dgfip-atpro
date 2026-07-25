# Contrat — Modèles de données

> Modèles métier et résultats de parsing exposés pour `v0.1.0`.

Package : `atpro`  
Référence : FEAT-005.1 / FEAT-003.1

## Modèles domaine

| Classe | Import | Rôle |
|---|---|---|
| `Site` | `from atpro.domain.sites import Site` | Site / plate-forme |
| `Agent` | `from atpro.domain.agents import Agent` | Agent |
| `AgentAlias` | `from atpro.domain.agents import AgentAlias` | Alias de nom agent |
| `AgentSiteAssignment` | `from atpro.domain.agents import AgentSiteAssignment` | Affectation agent ↔ site |
| `Call` | `from atpro.domain.calls import Call` | Appel consolidé |
| `CallSegment` | `from atpro.domain.calls import CallSegment` | Segment / ligne d'appel |
| `Ticket` | `from atpro.domain.tickets import Ticket` | Ticket |
| `AgentDailyActivity` | `from atpro.domain.activities import AgentDailyActivity` | Activité journalière agent |

Ce sont des dataclasses figées (`frozen=True`) avec validation via `DomainError`.

## Résultats de parsing

| Classe | Import | Rôle |
|---|---|---|
| `ParseResult` | `from atpro.parser.results import ParseResult` | Résultat complet |
| `ParsePreview` | `from atpro.parser.results import ParsePreview` | Aperçu borné |
| `ParseIssue` | `from atpro.parser.results import ParseIssue` | Diagnostic unitaire |
| `FileMetadata` | `from atpro.parser.results import FileMetadata` | Métadonnées fichier |
| `ParseSummary` | `from atpro.parser.results import ParseSummary` | Synthèse (compteurs, statut) |
| `ImportError` | `from atpro.parser.results import ImportError` | Erreur structurée (non exception) |
| `ImportWarning` | `from atpro.parser.results import ImportWarning` | Avertissement structuré |

## Enums utiles

Sous `atpro.domain.enums` : `ImportFileType`, `SchemaVersion`, `ParseStatus`,
`ImportSeverity`, `CallDirection`, `PeriodType`, `ScopeType`.

## Hors modèles v0.1.0

Entités de persistence, DTO HTTP, modèles de statistiques / rapports.
