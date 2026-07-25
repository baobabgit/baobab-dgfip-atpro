# Echantillons de reference (anonymises)

Ce dossier est reserve aux **echantillons CSV anonymises** explicitement
autorises a etre versionnes.

## Regles

- **Ne jamais** y placer d'exports reels contenant des donnees personnelles
  ou metier sensibles.
- Les fichiers `*.csv` de ce dossier sont **ignores par Git**
  (voir `.gitignore`) : seuls `README.md` et `.gitkeep` sont versionnes.
- Pour valider des CSV reels hors depot, utiliser la variable
  `ATPRO_REFERENCE_CSV_DIR` (voir `docs/reference-data.md`).

## Decision v0.1.0

La CI s'appuie uniquement sur `tests/fixtures/csv/`. La validation locale
optionnelle passe par `pytest -m reference` / `make reference-test`.
