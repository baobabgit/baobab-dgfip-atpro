# Contrat CLI v0.1.0

Commande racine : `atpro`  
Point d'entrée : `atpro.interfaces.cli.app:run` (`pyproject.toml` → `[project.scripts]`)  
Référence : FEAT-002.5

## Commandes publiques

```bash
atpro file inspect <path> [--json] [--verbose]
atpro file validate <path> [--json] [--verbose]
atpro file preview <path> [--limit N] [--json] [--verbose]
```

| Commande | Cas d'usage Python | Description |
|---|---|---|
| `inspect` | `ParseFileUseCase.inspect` | Type, schéma, encodage, séparateur |
| `validate` | `ParseFileUseCase.parse` | Validation / parsing complet |
| `preview` | `ParseFileUseCase.preview` | Aperçu des N premiers enregistrements |

## Options

| Option | Portée | Défaut | Effet |
|---|---|---|---|
| `--json` | toutes | off | Sortie JSON structurée |
| `--limit` | `preview` uniquement | `10` | Nombre max d'enregistrements |
| `--verbose` | toutes | off | Détails supplémentaires (toujours masqués si sensibles) |

## Codes de sortie

Enum : `atpro.interfaces.cli.exit_code.ExitCode`

| Code | Constante | Signification |
|---:|---|---|
| 0 | `SUCCESS` | Succès |
| 1 | `INVALID_FILE` | Fichier invalide (erreurs de parsing / statut FAILED) |
| 2 | `MISSING_OR_UNREADABLE` | Fichier introuvable, vide ou illisible (FATAL) |
| 3 | `UNKNOWN_FORMAT` | Format / schéma inconnu (`FILE_TYPE_UNKNOWN`) |
| 4 | `TECHNICAL_ERROR` | Erreur technique inattendue |

Dérivation : `ExitCode.from_parse_result` / `ExitCode.from_parse_preview`.

## Architecture CLI

```text
atpro (Typer)
 └── file (file_commands)
      └── FileCliService  →  ParseFileUseCase
           └── CliPresenter (texte / JSON, masquage)
```

- Le CLI appelle les cas d'usage Python ; **aucune logique métier** dans Typer.
- Le CLI **ne persiste aucune donnée**.
- Les sorties longues ne doivent pas afficher de données sensibles brutes
  (`SensitiveValueMasker`).

## Exemples

```bash
# Après uv sync / make install
uv run atpro file inspect tests/fixtures/csv/incoming_calls_valid.csv
uv run atpro file validate tests/fixtures/csv/incoming_calls_valid.csv --json
uv run atpro file preview tests/fixtures/csv/incoming_calls_valid.csv --limit 5
```

## Hors périmètre CLI v0.1.0

- sous-commandes `report`, `import` base, API, authentification ;
- écriture en base ou génération de PDF.
