# Tests report — BL-025

## Gates locaux

| Gate | Resultat |
|---|---|
| black | OK |
| ruff check | OK |
| mypy | OK |
| bandit | OK |
| pytest cov ≥ 95 % | OK — **339 passed**, **1 skipped**, couverture **97.56 %** |
| check_traceability | OK |
| twine check | OK |

## Criteres FEAT-016.1

- Engine depuis URL valide — OK
- Session creation / fermeture — OK
- Rollback sur exception (`session_scope`) — OK
- Import modules sans effet reseau — OK
