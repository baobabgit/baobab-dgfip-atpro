# Tests report — BL-016

## Commandes

```
uv run black src tests
uv run ruff check src tests
uv run mypy src
uv run bandit -r src -c pyproject.toml -q
uv run pytest -q --cov=src --cov-fail-under=95
```

## Resultat

- black / ruff / mypy / bandit : OK
- pytest : **237 passed**
- couverture globale : **96.40 %**
- `ParseFileUseCase` : **100 %** (fichier source)
- tests orchestration : **21** dans `test_parse_file_use_case.py`
