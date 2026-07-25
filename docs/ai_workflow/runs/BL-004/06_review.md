# Revue — BL-004

## TESTER: GO
## REVIEWER: GO

Critères vérifiés :

- Enums FEAT-005.2 : `PeriodType`, `ScopeType`, `ImportFileType`, `CallDirection`,
  `ImportSeverity`, `ParseStatus`, `SchemaVersion`.
- Value objects : `DurationSeconds`, `Percentage`, `DateRange`, `FileSha256`.
- Conversions invalides → `DomainError` (pas de masquage silencieux).

CI: verte (qualité, tests, build, traçabilité, politique commit).
PR: https://github.com/baobabgit/baobab-dgfip-atpro/pull/12
Merge: 2026-07-25T10:57:33Z
