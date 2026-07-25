# Tests report — BL-017

## Gates

| Gate | Resultat |
|---|---|
| black --check | OK |
| ruff check | OK |
| mypy src | OK |
| bandit | OK |
| pytest cov ≥ 95 % | OK — 266 passed, couverture totale **96.74 %** |

## Tests CLI (FEAT-002.5)

- `test_FEAT_002_5_inspect_success`
- `test_FEAT_002_5_validate_success`
- `test_FEAT_002_5_preview_success`
- `test_FEAT_002_5_missing_file_exit_2`
- `test_FEAT_002_5_unknown_format_exit_3`
- `test_FEAT_002_5_json_output_valid`

Package CLI couvert a 100 % (sauf 2 branches `if text` deja exercees via inspect).
