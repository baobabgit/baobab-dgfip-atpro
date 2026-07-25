# Tests report — BL-018

## Gates

| Gate | Resultat |
|---|---|
| black --check | OK |
| ruff check | OK |
| mypy src | OK |
| bandit | OK |
| pytest cov ≥ 95 % | OK — 279 passed, couverture totale **96.74 %** |

## Tests fixtures (FEAT-012.1)

- Valides : incoming, outgoing, tickets long/short, activities wide/long
- Invalides : `CALL_END_BEFORE_START`, `TICKET_RESOLVED_BEFORE_CREATED`, `ACTIVITY_MEASURE_CONFLICT`
- `unknown_format` → `FILE_TYPE_UNKNOWN` via `ParseFileUseCase`
- Readers incoming + tickets long consomment les fixtures versionnees
