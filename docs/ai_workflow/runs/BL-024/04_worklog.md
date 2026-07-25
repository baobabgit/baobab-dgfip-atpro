# Worklog — BL-024

## 2026-07-25

- Branche `bl/024-postgres-compose` depuis `version/v0.2.0`.
- Ajoute `compose.yml` : image `postgres:17`, volume `atpro_postgres_data`,
  healthcheck, port `${ATPRO_DATABASE_PORT:-5432}`.
- Documentation `docs/operations/database.md` (up/stop/down -v / logs / limites).
- Tests structurels YAML + presence doc.
- `docker compose config` OK en local.
- Bookkeeping : BL-023 DONE dans queue.
- Suite pytest complete OK ; PR #42 ; CI verte ; verdicts GO ; merge squash.
- Micro-PR #43 : BL-024 DONE, BL-025 READY, verrou libere.
