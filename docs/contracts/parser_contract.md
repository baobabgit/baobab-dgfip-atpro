# Contrat parseur CSV v0.1.0

## Entrees

- chemin de fichier CSV ;
- encodage detecte ou fourni ;
- separateur detecte ou fourni ;
- option de limite pour preview.

## Sorties

- `FileInspection` pour l'inspection ;
- `ParseResult` pour validation et parsing ;
- `ParsePreview` pour apercu.

## Types de fichiers supportes

- appels entrants ;
- appels sortants ;
- tickets ;
- activites agents format large ;
- activites agents format long.

## Comportements obligatoires

- detection par colonnes et contenu, pas uniquement par nom ;
- consolidation des appels multi-lignes ;
- conservation de la provenance ligne ;
- erreurs et avertissements structures ;
- masquage des donnees sensibles dans les diagnostics ;
- pas d'acces base de donnees.

## Validation reference

Les fixtures anonymisees sont obligatoires pour la CI.

Les CSV reels sont optionnels et cadres par `docs/reference-data.md`.
