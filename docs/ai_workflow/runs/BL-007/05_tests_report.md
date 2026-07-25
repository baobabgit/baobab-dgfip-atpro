# Tests report — BL-007

## Gates

- `black --check` : OK
- `ruff check` : OK
- `mypy src` : OK
- `bandit` : OK (0 finding)
- `pytest --cov-fail-under=95` : OK (79 passed, couverture ~97 %)
- `uv build` + `twine check` : OK
- `check_traceability` : OK

## Couverture des criteres BL

- UTF-8 / Windows-1252 / separateur `;` / vide / absent : couverts
- SHA-256 streaming et stabilite : couverts
- Normalisation accents / guillemets : couverts
