# Expected outputs — BL-020

1. Contrats : `public_api.md`, `parser_contract.md`, `cli_contract.md`,
   `models.md`, `imports.md`, `services.md`, `exceptions.md`
2. `docs/integrations/compatibility_matrix.yaml` (domain/parser/cli delivered)
3. `README.md` aligné sur le package AT Pro
4. Guides : `cli-file.rst`, `perimetre-v010.rst`, `premiers-pas.rst` mis à jour,
   `ajouter-une-classe.rst` sans chemins template, `guides/index.rst`
5. Run `docs/ai_workflow/runs/BL-020/` (00–05 + status.yaml)
6. Aucune occurrence `example_package` / `Greeter` / template `Repository` dans
   `docs/contracts`
7. Gates verts (black, ruff, mypy, pytest cov ≥ 95 %)
