# Tests report — BL-021

## Gates

| Gate | Resultat |
|---|---|
| black | OK |
| ruff check | OK |
| mypy src | OK |
| bandit | OK |
| pytest cov ≥ 95 % | OK — **320 passed**, **1 skipped**, couverture **97.47 %** |
| traceability | OK |

## Marqueur `reference`

| Commande | Resultat |
|---|---|
| `pytest -q -m reference --no-cov` (env absent) | **1 skipped**, exit 0 |
| meme commande + `-W error::pytest.PytestUnknownMarkWarning` | OK (pas de warning) |
| env set, dossier vide | **1 failed** (`dossier reference vide`) |

## Couverture BL-021

- `atpro.testing.reference_data_locator` : **100 %**
- Suite CI : le test reference est skippe (pas de faux vert)
