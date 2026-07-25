# Contrat public Python v0.1.0

Package : `atpro`  
Version cible : `v0.1.0`

## Objectif

Ce contrat remplace le contrat template. Il decrit l'API publique attendue du package `atpro` pour le lot `v0.1.0`.

## Modules publics attendus

```text
atpro.domain
atpro.parser
atpro.interfaces.cli
```

## Modeles publics attendus

Le package doit exposer ou rendre importables les modeles suivants :

- `Site`
- `Agent`
- `AgentAlias`
- `AgentSiteAssignment`
- `Call`
- `CallSegment`
- `Ticket`
- `AgentDailyActivity`
- `FileMetadata`
- `ParseResult`
- `ParsePreview`
- `ParseIssue`

## Cas d'usage public attendu

```python
from pathlib import Path

from atpro.parser import ParseFileUseCase

use_case = ParseFileUseCase()
inspection = use_case.inspect(Path("appels.csv"))
result = use_case.parse(Path("appels.csv"))
preview = use_case.preview(Path("appels.csv"), limit=10)
```

## Contraintes

- Le domaine ne depend pas de SQLAlchemy, FastAPI, Typer, Polars ou Quarkdown.
- Le parsing ne depend pas de PostgreSQL.
- Les resultats sont serialisables.
- Les erreurs sont structurees et testables.

## Hors contrat v0.1.0

- API HTTP ;
- persistence ;
- statistiques ;
- rapports ;
- interface React.
