# Validation v0.1.0

## Gates avant developpement

- `ADR-0001` existe dans `docs/architecture/adr/`.
- `queue.yaml` contient les items `BL-001` a `BL-021`.
- Le dossier de version contient `version.yaml`, `scope.md`, `validation.md`, `integration_matrix.yaml`, `release_report.md`.
- Les fiches utilisent les conventions `US-XXX`, `FEAT-XXX.Y`, `BL-XXX`.
- Les contrats publics ne referencent plus le template `example_package`, `Greeter` ou `Repository`.

## Gates pendant developpement

- Chaque backlog demarre avec un fichier `docs/ai_workflow/runs/BL-XXX/status.yaml`.
- Les warnings de tests sont corriges ou explicitement justifies.
- Le marqueur Pytest `reference` est declare dans `pyproject.toml` des que les tests de reference sont ajoutes.
- Les fichiers sous `sources/` restent en lecture seule.

## Gates de sortie

- `make all` passe.
- `make traceability` passe.
- Les fixtures anonymisees couvrent toutes les familles de CSV.
- La validation sur CSV reels est documentee et ne produit pas de faux succes en leur absence.
- Les contrats publics documentent les modeles et interfaces livres.
- Le rapport de release est mis a jour.
