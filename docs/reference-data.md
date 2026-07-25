# Donnees de reference CSV

Projet : AT Pro Pilotage  
Version cible : `v0.1.0`

## Objectif

Ce document precise comment fournir les fichiers CSV reels de reference sans les supposer presents dans le depot et sans ajouter de donnees sensibles versionnees.

## Regle par defaut

La CI doit utiliser des fixtures anonymisees versionnees dans `tests/fixtures/csv/`.

Les fichiers CSV reels de reference sont optionnels et doivent etre fournis localement par l'une des modalites suivantes :

- variable d'environnement `ATPRO_REFERENCE_CSV_DIR` pointant vers un dossier local hors depot ;
- volume externe dans un environnement Docker futur ;
- dossier `samples/reference/` uniquement si les fichiers sont anonymises et autorises a etre versionnes ;
- stockage documentaire hors depot avec procedure de copie locale.

## Comportement attendu

Si `ATPRO_REFERENCE_CSV_DIR` est absent :

- les tests unitaires et CI doivent continuer avec les fixtures anonymisees ;
- les tests marques `reference` doivent etre ignores explicitement ou signaler que la validation de reference n'a pas ete executee ;
- aucun controle ne doit afficher un succes trompeur sur les fichiers reels.

Si `ATPRO_REFERENCE_CSV_DIR` pointe vers un dossier vide :

- la commande de validation de reference doit produire un message explicite ;
- le resultat ne doit pas etre confondu avec une validation reussie.

Si `ATPRO_REFERENCE_CSV_DIR` contient les CSV reels :

- les parseurs doivent inspecter, valider et previsualiser les fichiers disponibles ;
- les anomalies doivent etre reportees avec le nom du fichier et le type detecte ;
- les donnees sensibles ne doivent pas etre affichees en clair dans les logs longs.

## Commande recommandee

```bash
pytest -m reference
```

Le marqueur doit etre declare dans `pyproject.toml` des que Pytest est configure :

```toml
[tool.pytest.ini_options]
markers = [
    "reference: tests optionnels utilisant les CSV reels de reference",
]
```

Si d'autres marqueurs existent deja, ajouter `reference` a la liste existante sans supprimer les autres.

ou, si le CLI est disponible :

```bash
atpro file validate "%ATPRO_REFERENCE_CSV_DIR%"
```

## Points ouverts

- Valider si des echantillons anonymises peuvent etre ajoutes dans `samples/reference/`.
- Definir le nom exact du marqueur Pytest `reference`.
- Definir si une absence de CSV reels doit etre un skip ou une erreur dans les environnements de recette.
