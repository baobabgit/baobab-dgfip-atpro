# Contrat — Exceptions publiques

> Exceptions et diagnostics publics du package `atpro` (v0.1.0).

## Exceptions Python

| Classe | Module | Usage |
|---|---|---|
| `DomainError` | `atpro.domain.exceptions` | Erreurs métier domaine (validation modèles) |
| `FileDetectionError` | `atpro.parser.detection` | Fichier absent, vide, illisible |
| `NormalizationError` | `atpro.parser.normalizers` | Valeur CSV non normalisable |

## Diagnostics structurés (pas des exceptions)

| Classe | Module | Usage |
|---|---|---|
| `ParseIssue` | `atpro.parser.results` | Code + message + sévérité + ligne |
| `ImportError` | `atpro.parser.results` | Erreur d'import (ERROR / FATAL) |
| `ImportWarning` | `atpro.parser.results` | Avertissement d'import |

Le CLI mappe ces diagnostics vers des codes de sortie (`ExitCode`) — voir
[`cli_contract.md`](cli_contract.md).

## Notes SemVer

Les exceptions et codes d'issue publics font partie du contrat API. Tout
changement incompatible (suppression de code, rupture de signature) est soumis
aux règles SemVer décrites dans [`compatibility.md`](compatibility.md).
