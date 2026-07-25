# Contexte — BL-001

## Etat au demarrage

- Depot template avec package `example_package`.
- Verrou libre ; aucun run existant.
- File `queue.yaml` : BL-001 READY, BL-002..BL-021 TODO.
- Artefacts de cadrage deja presentes en working tree (non commits) :
  fiches US/FEAT/BL, version v0.1.0, contrats, cahier des charges.

## Objectif

Trancher la structure du lot v0.1.0 via ADR-0001 avant tout code significatif.

## Contraintes

- Respecter `AGENTS.md` (mono-package `src/<package>`, Git 3 niveaux).
- Ne pas contredire le cahier des charges sans justification explicite.
- `frontend/`, Docker applicatif, FastAPI, worker, PostgreSQL hors v0.1.0.
