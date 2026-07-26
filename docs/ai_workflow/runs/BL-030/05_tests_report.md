# Tests report — BL-030

## Gates

- `black --check` : OK
- `ruff check` : OK
- `mypy src` : OK
- `bandit -r src` : OK
- `pytest --cov-fail-under=95` : OK (374 passed, 1 skipped, ~97.8 %)

## Cas couverts

- Creation site / agent
- Reimport identique (EXISTING, pas de doublon)
- Conflit de cle metier
- Recherche par id / nom canonique
- Liste incluant inactifs
- Roundtrip mappers
- UoW expose sites/agents
