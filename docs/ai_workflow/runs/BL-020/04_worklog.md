# Worklog — BL-020

- Branche `bl/020-document-v010`, verrou BUSY (developpeur / cursor)
- Contrats publics réécrits pour `atpro` v0.1.0 :
  - `public_api.md` — ParseFileUseCase + chemins d'import
  - `parser_contract.md` — schemas, readers, orchestrateur, normalizers
  - `cli_contract.md` — FEAT-002.5 (options, exit codes)
  - `models.md`, `imports.md`, `services.md`, `exceptions.md`
- `compatibility_matrix.yaml` : domain/parser/cli = `delivered` ;
  database/api/frontend/reports = `out_of_scope`
- `README.md` : package AT Pro (install uv, CLI, qualité, contrats)
- Guides RST : `cli-file.rst`, `perimetre-v010.rst`, `premiers-pas.rst`,
  `ajouter-une-classe.rst` ; toctree `guides/index.rst`
- Run docs `docs/ai_workflow/runs/BL-020/` (00–05 + status.yaml)
- Aucune modification `src/` / `tests/`
- Gates : black, ruff, mypy, pytest 314 passed / cov **97.43 %**
- Aucun commit (demande explicite)
