# Tests report — BL-024

## Gates locaux

| Gate | Resultat |
|---|---|
| pytest structurel compose/docs | OK (2 passed) |
| `docker compose config` | OK |
| pytest cov ≥ 95 % (suite) | OK — **332 passed**, **1 skipped**, couverture **97.53 %** |

## Criteres FEAT-015.1

- Service PostgreSQL 17 declare — OK
- Volume + healthcheck — OK
- Port configurable — OK
- Pas de secret production — OK
- Doc demarrage / arret / nettoyage volume — OK

## CI PR #42

Verte (qualite, tests, tracabilite, build).
