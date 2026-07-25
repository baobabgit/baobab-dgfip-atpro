# Expected outputs — BL-023

- Dependances : `sqlalchemy`, `alembic`, `psycopg[binary]` (+ lockfile)
- `src/atpro/infrastructure/config/` :
  - `DatabaseSettings`
  - `DatabaseUrlMasker`
  - `DatabaseConfigurationError`
- Tests unitaires URL explicite / assemblage / erreur / masquage
- `.env.example` mis a jour
- Marqueurs pytest `postgres` et `integration` dans `pyproject.toml`
