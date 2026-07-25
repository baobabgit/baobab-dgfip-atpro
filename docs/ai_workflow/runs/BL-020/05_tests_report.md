# Tests report — BL-020

## Gates

| Gate | Résultat |
|---|---|
| black --check src tests | OK |
| ruff check src tests | OK |
| mypy src | OK |
| pytest cov ≥ 95 % | OK — **314 passed**, couverture **97.43 %** |
| `rg -i "example_package\|Greeter\|Repository" docs/contracts` | OK — aucun match |

## Note

BL-020 est documentation uniquement : aucun test applicatif ajouté.
Les gates confirment l'absence de régression sur le code existant.
