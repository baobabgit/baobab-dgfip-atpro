# Worklog — BL-019

- Branche `bl/019-parser-non-regression`, verrou BUSY (developpeur)
- Suite non-regression sous `tests/unit/atpro/regression/` :
  - `test_non_regression_fixtures_pipeline.py` — inspect/validate/parse/preview
    pour chaque `*.csv` de `tests/fixtures/csv/`
  - `test_non_regression_cli.py` — CliRunner `atpro file inspect|validate|preview`,
    codes 0/1/2/3
  - `test_non_regression_errors.py` — codes ImportError, FileDetectionError via
    use case, DomainError FileMetadata/ParseIssue/Import*, PARTIAL ParseResult
- Aucune modification de code production
- Gates : black, ruff, mypy, bandit, pytest 314 passed / cov **97.43 %**
- `uv run nox -s all` OK (quality + test + build + traceability ; `make` absent sur Windows)
- Aucun commit (demande explicite)
