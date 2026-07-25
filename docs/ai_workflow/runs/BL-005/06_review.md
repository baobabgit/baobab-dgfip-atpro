# Revue — BL-005

## TESTER: GO
## REVIEWER: GO

Critères vérifiés :

- Modèles : `Site`, `Agent`, `AgentAlias`, `AgentSiteAssignment`, `Call`,
  `CallSegment`, `Ticket`, `AgentDailyActivity`.
- Champs de provenance (`source_import_batch_id`, `line_fingerprint`,
  `source_row_numbers`).
- Dataclasses frozen, validation des champs obligatoires, aucune dépendance
  SQLAlchemy / FastAPI / Typer / Polars.

CI: verte (qualité, tests, build, traçabilité, politique commit).
PR: https://github.com/baobabgit/baobab-dgfip-atpro/pull/13
Merge: 2026-07-25T11:52:03Z
