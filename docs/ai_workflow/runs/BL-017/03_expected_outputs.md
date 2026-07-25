# Expected outputs — BL-017

- `src/atpro/interfaces/cli/` (app, file_commands, exit_code, presenter, service)
- `atpro = "atpro.interfaces.cli.app:run"` dans `pyproject.toml`
- Dependance `typer` (+ lock)
- Tests `tests/unit/atpro/interfaces/cli/`
- Gates : black, ruff, mypy, bandit, pytest cov ≥ 95 %
