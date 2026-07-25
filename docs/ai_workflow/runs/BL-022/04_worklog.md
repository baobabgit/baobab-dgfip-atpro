# Worklog — BL-022

## 2026-07-25

- Reprise branche `bl/022-adr-persistance` (deja ouverte depuis `version/v0.2.0`).
- Relu ADR-0001, scope v0.2.0, contrat de persistance, FEAT-014.1, US-014, CDC §8.
- Redige ADR-0002 : structure `src/atpro`, couches, stack PostgreSQL/SQLAlchemy/
  Alembic/UoW, idempotence, politique conservative, cycle d'import, rollback,
  hors perimetre, divergence CDC §8.5 (stats reportees).
- Exigence ADR-0002 ajoutee dans `scripts/check_traceability.py`.
- Gates documentaires : `check_traceability.py` OK.
- PR #40 ouverte, CI verte, verdicts TESTER/REVIEWER GO, merge squash.
