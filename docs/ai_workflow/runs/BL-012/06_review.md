# Revue — BL-012

## TESTER

| Critere | Verdict | Preuve |
|---|---|---|
| Fichier valide deux mesures | GO | `test_FEAT_005_4_valid_file_two_measures` |
| Date historique | GO | `test_FEAT_005_4_historical_date_format` |
| Multi-lignes | GO | `test_FEAT_005_4_multi_line_call` |
| Multi-segments | GO | `test_FEAT_005_4_multi_segments` |
| Flux / service | GO | asserts `flow` / `service` sur Call |
| Schema incompatible | GO | `SCHEMA_NOT_INCOMING` / `SCHEMA_INCOMING_REQUIRED` |
| CI couverture ≥ 95 % | GO | job Tests + couverture SUCCESS |

**Verdict TESTER : GO**

## REVIEWER

- Reutilise `CallConsolidator` / `CallFieldMapper` (BL-011) — pas de duplication.
- Direction forcee `INCOMING`.
- Une classe par fichier, injection des collaborateurs.
- Scope respecte (`parser/readers` + exports + run workflow).

**Verdict REVIEWER : GO**
