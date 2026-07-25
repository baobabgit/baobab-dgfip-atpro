# Contrat public Python v0.1.0

Package : `atpro`  
Version cible : `v0.1.0`  
Référence : FEAT-001.2 / FEAT-002.4 / FEAT-005.1

## Objectif

Décrire l'API publique stable du package `atpro` pour le lot `v0.1.0`
(parseurs CSV + modèles métier + CLI fichier). Aucune référence au squelette
template.

## Modules publics

```text
atpro                  # __version__, domain, parser, interfaces
atpro.domain           # modèles et enums métier
atpro.parser           # ParseFileUseCase + sous-packages
atpro.interfaces.cli   # app Typer (console_scripts: atpro)
```

## Cas d'usage public

```python
from pathlib import Path

from atpro.parser import ParseFileUseCase

use_case = ParseFileUseCase()
inspection = use_case.inspect(Path("appels.csv"))
result = use_case.parse(Path("appels.csv"))
preview = use_case.preview(Path("appels.csv"), limit=10)
```

Méthodes de `ParseFileUseCase` :

| Méthode | Retour | Rôle |
|---|---|---|
| `inspect(path)` | `FileInspection` | Type, schéma, encodage, séparateur |
| `parse(path)` / `validate(path)` | `ParseResult` | Parsing / validation complète |
| `preview(path, limit=10)` | `ParsePreview` | Aperçu borné |

## Imports de modèles (chemins garantis)

```python
from atpro.domain.sites import Site
from atpro.domain.agents import Agent, AgentAlias, AgentSiteAssignment
from atpro.domain.calls import Call, CallSegment
from atpro.domain.tickets import Ticket
from atpro.domain.activities import AgentDailyActivity

from atpro.parser.results import (
    FileMetadata,
    ParseIssue,
    ParsePreview,
    ParseResult,
    ParseSummary,
    ImportError,
    ImportWarning,
)
from atpro.parser.detection import FileInspection, FileDetectionError
from atpro.parser import ParseFileUseCase
```

Détail des modèles : [`models.md`](models.md).  
Détail parseur : [`parser_contract.md`](parser_contract.md).  
Détail CLI : [`cli_contract.md`](cli_contract.md).

## Contraintes

- Le domaine ne dépend pas de SQLAlchemy, FastAPI, Typer, Polars ou Quarkdown.
- Le parsing ne dépend pas de PostgreSQL.
- Les résultats (`ParseResult`, `ParsePreview`, diagnostics) sont sérialisables.
- Les erreurs sont structurées et testables (`ParseIssue`, codes stables).

## Hors contrat v0.1.0

- API HTTP ;
- persistence / base de données ;
- statistiques et rapports ;
- interface React.
