# ADR-0002 - Persistance PostgreSQL v0.2.0

Statut : accepte  
Date : 25 juillet 2026  
Version cible : `v0.2.0`  
Backlog lie : `BL-022`  
References : `US-014`, `FEAT-014.1`, `ADR-0001`

## Contexte

Le lot `v0.1.0` a livre le package Python `atpro` sous `src/atpro/` : modeles
metier canoniques, parseurs CSV, resultat `ParseResult`, CLI `file`, fixtures
anonymisees. La persistance etait explicitement hors perimetre (`ADR-0001`).

Le cahier des charges (section 8) exige ensuite d'enregistrer ces modeles dans
PostgreSQL sans doublons, avec provenance, diagnostics d'import et rollback
controle. Le lot `v0.2.0` doit introduire cette couche sans casser le contrat
librairie mono-package ni anticiper FastAPI, React, worker ou statistiques.

## Decision

### Structure depot

Pour `v0.2.0`, **`src/atpro` reste le coeur Python** (confirmation de
`ADR-0001`). Aucune migration vers `backend/src/atpro` dans ce lot.

Modules cibles a l'interieur du package :

```text
src/atpro/
  domain/                  # modeles et value objects (independants de SQLAlchemy)
  application/             # cas d'usage (ex. ImportParsedFile), ports repositories
  application/imports/     # orchestration d'import depuis ParseResult
  infrastructure/
    database/              # engine, sessions, UoW, modeles ORM, repositories SQLA
  interfaces/
    cli/                   # file (v0.1.0) + imports / referentiels (v0.2.0)
```

Regle de dependance :

- `domain` ne depend d'aucune couche ;
- `application` depend de `domain` et de ports abstraits ;
- `infrastructure.database` implemente les ports et depend de SQLAlchemy ;
- `interfaces.cli` appelle uniquement `application` (jamais l'ORM directement).

### Stack de persistance

| Composant | Role dans v0.2.0 |
|---|---|
| PostgreSQL 17+ | Base cible ; contraintes d'unicite portees par SQL |
| Docker Compose (dev) | Service PostgreSQL local avec volume, healthcheck, variables d'environnement |
| SQLAlchemy 2.x | Mapping ORM, engine, sessions |
| Alembic | Migrations versionnees du schema |
| Unit of Work | Une transaction applicative par cas d'usage d'import / rollback |
| Repositories | Acces aux agregats ; recivent des objets domaine, jamais des lignes CSV brutes |

Les modeles du domaine restent **independants de SQLAlchemy**. Les tables ORM
vivent exclusivement dans `infrastructure.database`.

### Idempotence

Les imports sont idempotents par **contraintes PostgreSQL** en premier, completees
par des empreintes applicatives :

1. empreinte SHA-256 du fichier source ;
2. cles metier uniques (sites, aliases, tickets, appels, segments, activites) ;
3. empreintes normalisees de contenu ;
4. ecriture dans une **transaction unique** par lot ;
5. `ON CONFLICT` pour inserer ou ignorer selon la politique.

Un reimport d'un fichier identique ne cree aucune ligne metier supplementaire.

### Politique de conflits (conservative)

Pour `v0.2.0`, une **politique globale conservative** s'applique :

- contenu normalise identique → ignorer (compteur `ignored`) ;
- contenu different sur cle metier existante → **ne pas ecraser automatiquement** ;
  tracer un conflit / rejet diagnostique (`conflicted` / quarantaine) ;
- aucun remplacement automatique des appels historiques ;
- configuration multi-niveaux (site, execution ponctuelle) **hors scope** de
  `v0.2.0` (reportable ulterieurement sans casser le schema).

La politique active d'un lot doit etre visible dans l'historique d'import.

### Cycle d'import

1. Creer un `import_batch` en statut `running`.
2. Rapprocher / inserer les referentiels (sites, agents, alias, affectations).
3. Inserer les donnees metier avec `ON CONFLICT`.
4. Enregistrer les lignes rejetees (payload masque).
5. Clore le lot (`completed`, `completed_with_warnings` ou `failed`).

En cas d'erreur bloquante : rollback de la transaction metier ; le lot reste
auditable.

### Rollback

L'annulation d'un lot est transactionnelle : desactive le lot, retire ou marque
comme annulees les donnees provenant **exclusivement** de ce lot, conserve les
diagnostics. Les donnees partagees avec d'autres lots ne sont pas detruites.

### Docker et application complete

`v0.2.0` prepare la cible dockerisee **sans la livrer entierement** :

- Compose de **developpement** pour PostgreSQL uniquement ;
- pas de stack production (API, frontend, Nginx, worker) ;
- le package `atpro` reste consommable hors Docker.

## Divergence documentee avec le cahier des charges

Le cahier des charges (section 8.5) mentionne l'invalidation des statistiques
lors d'un import. **Les statistiques restent hors `v0.2.0`** (scope version et
`FEAT-014.1`). L'ADR reporte donc l'etape "invalider les statistiques" a un lot
ulterieur ; l'import se termine sans calculer ni invalider de metriques.

## Decisions non reversibles (dans v0.2.0)

- PostgreSQL comme moteur de persistance.
- Contraintes d'unicite portees par SQL.
- Separation domaine / ORM.
- Unit of Work pour les cas d'usage d'ecriture.

## Decisions reversibles

- Politique de conflit strictement globale (extensible plus tard).
- Emplacement exact des modules sous `infrastructure.database`.
- Details des noms de tables / colonnes (figes par migrations Alembic).
- Compose dev uniquement (evolution vers stack complete via ADR ulterieur).

## Hors perimetre v0.2.0

- Statistiques site / agent ;
- API FastAPI ;
- Interface React ;
- Worker asynchrone ;
- Rapports Quarkdown ;
- Authentification et roles ;
- Docker applicatif de production complet ;
- Migration monorepo `backend/` / `frontend/`.

## Consequences

### Positives

- Les BL suivants (migrations, repositories, import, CLI) ont un cadre clair.
- Le parseur `v0.1.0` reste inchange en contrat ; `ParseResult` est l'entree
  d'import.
- La librairie reste testable : domaine sans base ; integration PostgreSQL via
  marqueurs dedies.

### Negatives

- La politique conservative peut augmenter le volume de conflits a traiter
  manuellement.
- L'absence de statistiques dans ce lot laisse un ecart temporaire avec le
  scenario CDC 8.5.

## Verification attendue

Avant le demarrage des migrations (`BL-027` et suivants) :

- `docs/architecture/adr/ADR-0002-persistance-postgresql-v020.md` existe ;
- `docs/contracts/persistence_contract.md` est aligne ;
- `docs/ai_workflow/versions/v0.2.0/` est initialise ;
- `python scripts/check_traceability.py` passe ;
- aucune contradiction non justifiee avec `ADR-0001`.
