# Donnees de reference CSV

Projet : AT Pro Pilotage  
Version cible : `v0.1.0`

## Decision v0.1.0 (tranchee)

| Contexte | Source de donnees | Comportement |
|---|---|---|
| **CI** | Fixtures anonymisees `tests/fixtures/csv/` uniquement | Suite pytest par defaut ; **aucun** CSV reel requis |
| **Local optionnel** | Variable `ATPRO_REFERENCE_CSV_DIR` → dossier hors depot | `pytest -m reference` ou `make reference-test` |
| **Depot Git** | Jamais de CSV reels sensibles | `.gitignore` ignore `samples/reference/*.csv` et `sources/` |

Les points ouverts precedents (marqueur, skip vs erreur) sont **clos** pour v0.1.0 :

- marqueur Pytest : `reference` (declare dans `pyproject.toml`) ;
- `ATPRO_REFERENCE_CSV_DIR` **absent** → `pytest.skip` explicite (pas un faux vert) ;
- dossier **configure mais vide** → `pytest.fail` (« dossier reference vide ») ;
- CSV presents → `ParseFileUseCase.inspect` / `validate` sur chaque `*.csv`.

## Objectif

Fournir les fichiers CSV reels de reference **sans** les versionner et **sans**
casser la CI, tout en evitant un succes trompeur quand la validation n'a pas
tour.

## Regle par defaut

La CI utilise exclusivement les fixtures anonymisees versionnees dans
`tests/fixtures/csv/`.

Les CSV reels de reference sont **optionnels** en local via :

```text
ATPRO_REFERENCE_CSV_DIR=<chemin local hors depot>
```

Modalites **non** utilisees pour des exports sensibles :

- volume Docker externe (reserve a une evolution future) ;
- `samples/reference/` — **uniquement** echantillons anonymises et autorises
  (voir ci-dessous) ;
- stockage documentaire hors depot + copie locale ponctuelle.

## `samples/reference/`

Dossier reserve aux **echantillons anonymises autorises** a etre versionnes.
Il contient un `README.md` et un `.gitkeep`. Les `*.csv` y sont ignores par
Git : ne jamais y deposer d'exports reels contenant des donnees personnelles
ou metier sensibles.

## Comportement attendu

Si `ATPRO_REFERENCE_CSV_DIR` est absent :

- les tests unitaires et la CI continuent avec les fixtures anonymisees ;
- les tests marques `reference` font un **skip** explicite
  (`ATPRO_REFERENCE_CSV_DIR absent`) ;
- aucun controle n'affiche un succes trompeur sur les fichiers reels.

Si `ATPRO_REFERENCE_CSV_DIR` pointe vers un dossier vide (ou sans `*.csv`) :

- la commande de validation echoue avec un message explicite
  (`dossier reference vide`) ;
- le resultat **ne doit pas** etre confondu avec une validation reussie.

Si `ATPRO_REFERENCE_CSV_DIR` contient des CSV :

- chaque `*.csv` est inspecte et valide via `ParseFileUseCase` ;
- les anomalies sont reportees avec le **nom de fichier**, le **type detecte**
  et le **code** d'erreur ;
- les valeurs brutes sensibles ne sont pas dumpes dans les logs de test.

## Commandes

```bash
# Suite CI / developpement (fixtures uniquement) — skip des tests reference
uv run pytest
# ou : make test

# Validation locale optionnelle (requiert ATPRO_REFERENCE_CSV_DIR)
# --no-cov : la suite filtree ne mesure pas 95 % de couverture globale
uv run pytest -q -m reference --no-cov
# ou : make reference-test
```

Marqueur declare dans `pyproject.toml` :

```toml
[tool.pytest.ini_options]
markers = [
    "reference: tests optionnels utilisant les CSV reels de reference",
]
```

Alternative CLI sur un fichier precis (hors marqueur) :

```bash
uv run atpro file validate "%ATPRO_REFERENCE_CSV_DIR%\mon_export.csv"
```

## Helper technique

Classe interne `atpro.testing.reference_data_locator.ReferenceDataLocator`
(non exportee dans le contrat public `atpro`) :

- lit `ATPRO_REFERENCE_CSV_DIR` ;
- `is_configured()` / `is_empty()` / `iter_csv_files()` / `resolve_dir()`.

## Interdictions

- Ne jamais committer de CSV reels sensibles.
- Ne pas modifier les fichiers sous `sources/` pour les besoins de ce backlog.
- Ne pas faire passer silencieusement un test reference parce que le dossier
  est absent ou vide.
