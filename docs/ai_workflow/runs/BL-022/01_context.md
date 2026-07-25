# Context — BL-022

Le lot `v0.1.0` a livre le package `atpro` (parseurs CSV, `ParseResult`, CLI
`file`) sans persistance. Le lot `v0.2.0` introduit PostgreSQL.

Avant toute implementation (deps, migrations, repositories), une ADR doit
cadrer :

- conservation de `src/atpro` (confirmation ADR-0001) ;
- frontieres `domain` / `application` / `infrastructure.database` / `interfaces.cli` ;
- role de SQLAlchemy, Alembic, Unit of Work et repositories ;
- strategie d'idempotence et politique conservative de conflits ;
- hors perimetre : stats, FastAPI, React, Quarkdown, Docker prod.

Sources : cahier des charges §8, `docs/contracts/persistence_contract.md`,
`docs/ai_workflow/versions/v0.2.0/scope.md`, FEAT-014.1, US-014.
