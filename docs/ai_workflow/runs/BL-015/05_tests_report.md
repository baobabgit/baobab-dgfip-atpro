# Tests report — BL-015

## Gates

- `uv run black src tests` : OK
- `uv run ruff check src tests` : OK
- `uv run mypy src` : OK
- `uv run pytest -q --cov=src --cov-fail-under=95` : OK (≥ 95 %)

## Couverture tests BL-015

- Wide (FEAT-008.1) : ligne complete, valeurs vides, % virgule, date FR, agent compose, schema
- Long (FEAT-009.1) : multi-mesures, inconnue, doublon identique, doublon contradictoire, schema
