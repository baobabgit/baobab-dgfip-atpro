# Base de donnees PostgreSQL (developpement)

Version cible : `v0.2.0`  
Compose : `compose.yml` (service `postgres` uniquement)

## Pre-requis

- Docker Desktop ou Docker Engine + plugin Compose
- Fichier `.env` base sur `.env.example` (jamais de secret de production)

## Variables utiles

| Variable | Defaut | Role |
|---|---|---|
| `ATPRO_DATABASE_HOST` | `localhost` | Hote vu depuis la machine hote |
| `ATPRO_DATABASE_PORT` | `5432` | Port local expose |
| `ATPRO_DATABASE_NAME` | `atpro` | Nom de la base |
| `ATPRO_DATABASE_USER` | `atpro` | Utilisateur applicatif |
| `ATPRO_DATABASE_PASSWORD` | `atpro` | Mot de passe **dev uniquement** |
| `ATPRO_DATABASE_URL` | (construit) | URL SQLAlchemy optionnelle |

URL typique depuis l'hote :

```text
postgresql+psycopg://atpro:atpro@localhost:5432/atpro
```

## Demarrage

```bash
cp .env.example .env
docker compose up -d postgres
docker compose ps
docker compose exec postgres pg_isready -U atpro -d atpro
```

Attendre le healthcheck (`healthy`) avant les migrations ou tests d'integration.

## Arret

```bash
docker compose stop postgres
```

## Nettoyage du volume

Supprime les donnees persistantes de developpement :

```bash
docker compose down
docker volume rm atpro_postgres_data
```

Alternative :

```bash
docker compose down -v
```

## Diagnostic

```bash
docker compose logs postgres --tail=100
docker compose exec postgres psql -U atpro -d atpro -c '\conninfo'
```

## Migrations Alembic

Precondition : PostgreSQL demarre et joignable (variables ci-dessus ou
`ATPRO_DATABASE_URL`).

```bash
# Appliquer toutes les revisions
make db-upgrade
# equivalent :
uv run alembic upgrade head

# Revenir a l'etat vide (baseline)
uv run alembic downgrade base

# Creer une nouvelle revision (apres BL-028+)
uv run alembic revision -m "add_import_tables"
```

Emplacements stables (chemins relatifs au depot, pas de chemin absolu) :

- `alembic.ini`
- `migrations/env.py` — URL via `DatabaseSettings`, metadata via `Base`
- `migrations/versions/` — revisions lisibles (`20260726_baseline`, …)

La revision `20260726_baseline` est vide : les tables metier arrivent avec
BL-028 / BL-029.

## Limites v0.2.0

- Pas d'image backend / frontend / Nginx / worker dans ce compose.
- Les credentials par defaut sont **uniquement** pour le developpement local.
- Les tests marques `postgres` / `integration` doivent pointer vers cette base
  (ou une instance temporaire equivalente) via `ATPRO_DATABASE_URL`.
