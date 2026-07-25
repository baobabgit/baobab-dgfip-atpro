# Worklog — BL-021

- Branche `bl/021-reference-csv`, verrou BUSY (developpeur)
- Decision v0.1.0 documentee dans `docs/reference-data.md` (points ouverts clos)
- Helper `ReferenceDataLocator` (`src/atpro/testing/`) — hors contrat public `atpro`
- Marqueur pytest `reference` declare dans `pyproject.toml`
- Tests :
  - `tests/unit/atpro/testing/test_reference_data_locator.py` (sans marqueur)
  - `tests/unit/atpro/regression/test_reference_csv_optional.py` (`@pytest.mark.reference`)
- `samples/reference/` : README + `.gitkeep` ; `*.csv` ignores
- `.gitignore` : `samples/reference/*.csv`, `sources/`
- `make reference-test` → `pytest -q -m reference --no-cov`
- README + `.env.example` pointent vers la convention
- Gates verts ; aucun commit (demande explicite)
