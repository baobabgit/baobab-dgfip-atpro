# Validation v0.1.0

## Gates avant developpement

- `ADR-0001` existe dans `docs/architecture/adr/`.
- `queue.yaml` contient les items `BL-001` a `BL-021`.
- Le dossier de version contient `version.yaml`, `scope.md`, `validation.md`, `integration_matrix.yaml`, `release_report.md`.
- Les fiches utilisent les conventions `US-XXX`, `FEAT-XXX.Y`, `BL-XXX`.
- Les contrats publics ne referencent plus le template `example_package`, `Greeter` ou `Repository`.

## Gates pendant developpement

- Chaque backlog demarre avec un fichier `docs/ai_workflow/runs/BL-XXX/status.yaml`.
- A la cloture d'un BL : `status.yaml` passe a `MERGED` avec `pr_url`, et
  `06_review.md` / `07_handoff.md` sont renseignes avant ou juste apres le merge.
- `queue.yaml` reste aligne (DONE / READY / IN_PROGRESS) avec la realite Git.
- Les warnings de tests sont corriges ou explicitement justifies.
- Le marqueur Pytest `reference` est declare dans `pyproject.toml` des que les tests de reference sont ajoutes (prevu BL-021).
- Les fichiers sous `sources/` restent en lecture seule.

## Avancement courant (2026-07-25)

- `BL-001`..`BL-006` : DONE / MERGED.
- Prochain executable : `BL-007`.

## Gates de sortie

- `make all` passe.
- `make traceability` passe.
- Les fixtures anonymisees couvrent toutes les familles de CSV.
- La validation sur CSV reels est documentee et ne produit pas de faux succes en leur absence.
- Les contrats publics documentent les modeles et interfaces livres.
- Le rapport de release est mis a jour.
