# Tests report — BL-019

## Gates

| Gate | Resultat |
|---|---|
| black | OK (reformat tests regression) |
| ruff check | OK |
| mypy src | OK |
| bandit | OK |
| pytest cov ≥ 95 % | OK — **314 passed**, couverture totale **97.43 %** |
| nox -s all | OK (build + twine + traceability) |

## Suite non-regression (FEAT-013.1)

- Pipeline fixtures : 1 + 11 (parametrize `*.csv`) = 12 tests
- CLI : 11 tests (exit 0/1/2/3 + inspect unknown)
- Erreurs / DomainError / PARTIAL : 12 tests
- **Total regression : 35 tests** (314 − 279 baseline BL-018)

## Couverture resultats

Modules `file_metadata`, `import_error`, `parse_issue`, `parse_result`,
`parse_summary` : **100 %** apres les extras BL-019.
