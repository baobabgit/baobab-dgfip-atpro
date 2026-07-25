# Revue — BL-006

## TESTER: GO
## REVIEWER: GO

Critères vérifiés :

- `ParseIssue`, `ImportWarning`, `ImportError`, `ParseSummary`.
- `FileMetadata`, `ParseResult`, `ParsePreview`.
- Sérialisation JSON stable (`to_json`, clés triées).
- `ImportSeverity.FATAL` ajouté pour FEAT-003.1.
- Point de vigilance : `atpro.parser.results.ImportError` homonyme du builtin
  Python — les readers devront importer via le chemin package explicite.

CI: verte (qualité, tests, build, traçabilité, politique commit).
PR: https://github.com/baobabgit/baobab-dgfip-atpro/pull/14
Merge: 2026-07-25T11:54:37Z
