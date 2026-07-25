# Worklog — BL-025

## 2026-07-26

- Branche `bl/025-sqlalchemy-engine` depuis `version/v0.2.0`.
- Modules database : naming convention, Base, EngineFactory, SessionFactory.
- Tests unitaires SQLite en memoire (sessions) + URL PostgreSQL (engine sans connect).
- Gates locaux : black, ruff, mypy, bandit, pytest cov ≥ 95 % (339 passed).
