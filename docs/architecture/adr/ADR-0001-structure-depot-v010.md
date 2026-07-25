# ADR-0001 - Structure depot et perimetre v0.1.0

Statut : accepte  
Date : 25 juillet 2026  
Version cible : `v0.1.0`  
Backlog lie : `BL-001`

## Contexte

Le cahier des charges AT Pro Pilotage decrit une application dockerisee multi-services a terme :

- coeur Python ;
- CLI ;
- API FastAPI ;
- worker ;
- PostgreSQL ;
- React ;
- Docker Compose ;
- rapports Quarkdown.

Le fichier `AGENTS.md` (source unique de verite des regles de developpement) impose
une trajectoire orientee librairie Python reutilisable, avec notamment :

- Python >= 3.13, POO, 1 classe = 1 fichier ;
- package sous `src/<package>` ;
- qualite bloquante : `black`, `ruff`, `mypy` strict, `bandit`, couverture >= 95 % ;
- gestion des dependances via `uv` et lockfile `uv.lock` ;
- modele Git a 3 niveaux (`main` -> `version/vX.Y.Z` -> `bl/XXX-description`) ;
- fiches de backlog dans `docs/backlog/` ;
- ADR dans `docs/architecture/adr/` ;
- queue active dans `docs/ai_workflow/state/queue.yaml`.

Le lot `v0.1.0` doit donc concilier la cible applicative long terme avec un premier
increment mono-package compatible avec le perimetre de `AGENTS.md`.

## Decision

Pour `v0.1.0`, le projet est cadre comme un **package Python reutilisable** nomme `atpro`.

Structure retenue pour le lot :

```text
src/atpro/
tests/
docs/backlog/user_stories/
docs/backlog/features/
docs/backlog/backlogs/
docs/architecture/adr/
docs/ai_workflow/state/
docs/ai_workflow/versions/v0.1.0/
docs/contracts/
docs/integrations/
```

La cible applicative dockerisee reste valide, mais elle est hors implementation pour `v0.1.0`.

Les composants suivants sont explicitement hors perimetre `v0.1.0` :

- PostgreSQL ;
- SQLAlchemy ;
- Alembic ;
- FastAPI ;
- React ;
- worker ;
- Docker applicatif complet ;
- generation Quarkdown ;
- statistiques.

## Consequences

### Positives

- Le premier lot est compatible avec le workflow IA du depot.
- Les parseurs et modeles peuvent etre testes sans infrastructure.
- Le package `atpro` pourra etre reutilise par le CLI, l'API et le worker dans les versions suivantes.
- `make traceability` peut verifier les fiches dans les emplacements attendus.

### Negatives

- La structure finale multi-services n'est pas encore materialisee.
- Un futur ADR devra trancher l'introduction eventuelle de `backend/`, `frontend/` et `docker/`.
- Les documents front-end et Docker restent des exigences futures, pas des artefacts de `v0.1.0`.

## Regles applicables

Perimetre `AGENTS.md` retenu pour `v0.1.0` :

1. Les user stories sont dans `docs/backlog/user_stories/` au format `US-XXX.md`.
2. Les features sont dans `docs/backlog/features/` au format `FEAT-XXX.Y.md`.
3. Les backlogs sont dans `docs/backlog/backlogs/` au format `BL-XXX.md`.
4. Les ADR sont dans `docs/architecture/adr/`.
5. Le backlog actif est declare dans `docs/ai_workflow/state/queue.yaml`.
6. Le graphe de dependances est declare dans `docs/ai_workflow/state/dependency_graph.yaml`.
7. Les contrats publics de librairie sont declares dans `docs/contracts/`.
8. Les compatibilites inter-modules sont declarees dans `docs/integrations/compatibility_matrix.yaml`.
9. Le package applicatif s'appelle `atpro` et vit sous `src/atpro/` (pas sous
   `backend/src/atpro` pour ce lot).
10. `frontend/`, Docker applicatif complet, FastAPI, worker et PostgreSQL restent
    hors `v0.1.0`, sans contredire le cahier des charges : ce sont des lots ulterieurs.

## Verification attendue

Avant tout developpement de code, les controles suivants doivent etre vrais :

- `docs/architecture/adr/ADR-0001-structure-depot-v010.md` existe ;
- `docs/ai_workflow/versions/v0.1.0/version.yaml` existe ;
- `docs/ai_workflow/state/queue.yaml` contient les items `BL-001` a `BL-021` ;
- les identifiants courts `US-XXX`, `FEAT-XXX.Y`, `BL-XXX` sont utilises ;
- aucune fiche active n'utilise les anciens identifiants intermediaires ;
- les CSV reels de reference sont cadres par `docs/reference-data.md`.

## Decision future attendue

Un ADR ulterieur devra etre cree avant l'introduction de l'application multi-services, notamment pour decider :

- conservation de `src/atpro` a la racine ou migration vers `backend/src/atpro` ;
- emplacement de `frontend/` ;
- structure Docker Compose ;
- relation entre package Python, API et worker.
