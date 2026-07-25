# Expected Outputs — BL-021

- `docs/reference-data.md` mis à jour (décision v0.1.0 close)
- Marqueur `reference` dans `pyproject.toml`
- `src/atpro/testing/reference_data_locator.py` (+ package testing)
- Tests miroir locator + `test_reference_csv_optional.py` (`@pytest.mark.reference`)
- `samples/reference/` (README + `.gitkeep`, pas de secrets)
- `.gitignore` : `samples/reference/*.csv`, `sources/`
- Lien README + `make reference-test`
- Gates : black, ruff, mypy, bandit, pytest cov ≥ 95 %
- `pytest -m reference` (env absent) → skip, exit 0
