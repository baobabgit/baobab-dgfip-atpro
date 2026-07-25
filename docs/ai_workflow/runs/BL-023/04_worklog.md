# Worklog — BL-023

## 2026-07-25

- Branche `bl/023-database-config` depuis `version/v0.2.0`.
- `uv add sqlalchemy alembic "psycopg[binary]"`.
- Modules :
  - `DatabaseSettings` (pydantic-settings, URL ou composants)
  - `DatabaseUrlMasker`
  - `DatabaseConfigurationError`
- Tests unitaires miroir (URL, assemblage, erreur, masquage, repr sure).
- `.env.example` : variables `ATPRO_DATABASE_*`.
- Marqueurs pytest `postgres` / `integration`.
- Bookkeeping : BL-022 DONE dans queue.
- Gates locaux verts ; PR #41 ; CI verte ; verdicts GO ; merge squash.
