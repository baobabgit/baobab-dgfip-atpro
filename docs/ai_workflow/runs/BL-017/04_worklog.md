# Worklog — BL-017

- Branche `bl/017-cli-minimal` (deja creee), verrou BUSY
- `uv add typer` (dependance projet) + `uv.lock`
- Package `atpro.interfaces.cli` : ExitCode, CliPresenter, FileCliService, commandes Typer
- Entry point console `atpro = atpro.interfaces.cli.app:run`
- Export `interfaces` dans `atpro.__init__`
- Tests unitaires + CliRunner (inspect/validate/preview, exit 2/3, JSON)
- Gates vertes : black, ruff, mypy, bandit, pytest 266 passed / cov 96.74 %
- Aucun commit (demande explicite)
