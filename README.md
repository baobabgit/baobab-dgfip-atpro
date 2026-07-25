# atpro

[![CI](https://github.com/baobabgit/baobab-dgfip-atpro/actions/workflows/ci.yml/badge.svg)](https://github.com/baobabgit/baobab-dgfip-atpro/actions/workflows/ci.yml)
[![Integration](https://github.com/baobabgit/baobab-dgfip-atpro/actions/workflows/integration.yml/badge.svg)](https://github.com/baobabgit/baobab-dgfip-atpro/actions/workflows/integration.yml)
[![Release](https://github.com/baobabgit/baobab-dgfip-atpro/actions/workflows/release.yml/badge.svg)](https://github.com/baobabgit/baobab-dgfip-atpro/actions/workflows/release.yml)
[![PyPI version](https://img.shields.io/pypi/v/atpro.svg)](https://pypi.org/project/atpro/)
[![Python versions](https://img.shields.io/pypi/pyversions/atpro.svg)](https://pypi.org/project/atpro/)
<!-- Badge Read the Docs : à réactiver une fois l'hébergement de doc configuré.
[![Documentation Status](https://readthedocs.org/projects/baobab-dgfip-atpro/badge/?version=latest)](https://baobab-dgfip-atpro.readthedocs.io/en/latest/)
-->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

> Librairie Python **`atpro`** (AT Pro Pilotage, DGFiP) : modèles métier et
> parseurs CSV + CLI `atpro file`. Règles de développement : [`AGENTS.md`](AGENTS.md).

## Table des matières

- [À propos](#à-propos)
- [Fonctionnalités v0.1.0](#fonctionnalités-v010)
- [Limites v0.1.0](#limites-v010)
- [Stack technique](#stack-technique)
- [Structure du projet](#structure-du-projet)
- [Installation](#installation)
- [CLI](#cli)
- [API Python](#api-python)
- [Qualité et tests](#qualité-et-tests)
- [Documentation](#documentation)
- [Contrats et intégration](#contrats-et-intégration)
- [Notes de version](#notes-de-version)
- [Sécurité](#sécurité)
- [Contribuer](#contribuer)
- [Licence](#licence)

## À propos

`atpro` est une **librairie consommable** pour inspecter, valider et parser les
exports CSV AT Pro (appels entrants / sortants, tickets, activités agents).
Le lot **v0.1.0** livre le domaine, le parseur et un CLI minimal — sans base de
données, sans HTTP et sans interface React.

## Fonctionnalités v0.1.0

- Modèles métier : `Site`, `Agent`, `Call`, `CallSegment`, `Ticket`,
  `AgentDailyActivity`, etc.
- Détection de schéma (6 signatures) + readers dédiés.
- Normalisation dates (`Europe/Paris`), durées, pourcentages, agents / sites,
  masquage des valeurs sensibles.
- Cas d'usage unique : `ParseFileUseCase` (`inspect` / `parse` / `preview`).
- CLI : `atpro file inspect|validate|preview` (codes de sortie 0–4).
- Fixtures anonymisées + suite de non-régression parseurs.

## Limites v0.1.0

Hors périmètre de cette version :

- pas de persistence / PostgreSQL ;
- pas d'API HTTP ;
- pas de statistiques ni de rapports ;
- pas d'interface React.

Questions ouvertes : section 22 du
[cahier des charges](docs/specifications/000_cahier-des-charges/000_specifications.md)
et guide [`docs/guides/how-to/perimetre-v010.rst`](docs/guides/how-to/perimetre-v010.rst).

## Stack technique

| Domaine        | Outil                                  |
| -------------- | -------------------------------------- |
| Langage        | Python ≥ 3.13                          |
| Environnement  | `uv` + lockfile `uv.lock`              |
| CLI            | `typer`                                |
| Format         | `black`                                |
| Lint           | `ruff`                                 |
| Typage         | `mypy` (strict)                        |
| Sécurité       | `bandit`                               |
| Tests          | `pytest` + `pytest-cov` (≥ 95 %)      |
| Documentation  | `sphinx` (+ `furo`), reStructuredText  |
| Config         | `pydantic-settings`                    |
| CI / Hooks     | GitHub Actions, `pre-commit`           |

## Structure du projet

```
.
├── AGENTS.md                 # Règles de développement
├── src/atpro/                # Code (1 classe par fichier)
│   ├── domain/               # Modèles et enums
│   ├── parser/               # Détection, schémas, readers, use case
│   └── interfaces/cli/       # CLI Typer
├── tests/unit/atpro/         # Tests miroir + regression/
├── tests/fixtures/csv/       # Fixtures anonymisées
├── docs/
│   ├── contracts/            # Contrats publics
│   ├── guides/               # Tutoriels + how-to (Diátaxis)
│   ├── specifications/       # Cahier des charges
│   └── ai_workflow/          # Workflow, runs, verrou
├── pyproject.toml
├── uv.lock
└── Makefile
```

## Installation

Prérequis : [uv](https://docs.astral.sh/uv/) et Python 3.13.

```bash
git clone https://github.com/baobabgit/baobab-dgfip-atpro.git
cd baobab-dgfip-atpro
make install
# équivalent : uv sync && uv run pre-commit install
```

Le script console `atpro` est enregistré via `[project.scripts]`.

## CLI

```bash
uv run atpro file inspect chemin/fichier.csv
uv run atpro file validate chemin/fichier.csv --json
uv run atpro file preview chemin/fichier.csv --limit 10
```

Codes de sortie : `0` succès, `1` invalide, `2` introuvable/illisible,
`3` format inconnu, `4` erreur technique.
Détail : [`docs/contracts/cli_contract.md`](docs/contracts/cli_contract.md) et
[`docs/guides/how-to/cli-file.rst`](docs/guides/how-to/cli-file.rst).

## API Python

```python
from pathlib import Path
from atpro.parser import ParseFileUseCase

uc = ParseFileUseCase()
result = uc.parse(Path("appels.csv"))
```

Contrats : [`docs/contracts/public_api.md`](docs/contracts/public_api.md).

## Qualité et tests

```bash
make all
# ou séparément :
uv run black --check src tests
uv run ruff check src tests
uv run mypy src
uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=95
uv build
```

Sous Windows sans `make` : `uv run nox -s all`.

## Documentation

```bash
make docs
# ou : uv run sphinx-build -b html docs docs/_build/html
```

Guides : [`docs/guides/`](docs/guides/).

## Contrats et intégration

- Contrats publics : [`docs/contracts/`](docs/contracts/)
- Matrice de compatibilité :
  [`docs/integrations/compatibility_matrix.yaml`](docs/integrations/compatibility_matrix.yaml)
- Workflow `integration.yml` sur les PR vers `version/**`

## Notes de version

Voir [`CHANGELOG.md`](CHANGELOG.md). Version déclarée dans `pyproject.toml` :
`0.1.0`.

## Sécurité

- Aucun secret dans le dépôt : `.env` gitignoré ; modèle [`.env.example`](.env.example).
- Masquage des emails / téléphones dans les diagnostics CLI et parseur.
- `bandit` + Dependabot. Signalez les vulnérabilités en privé
  ([`SECURITY.md`](SECURITY.md)).

## Contribuer

Règles : [`AGENTS.md`](AGENTS.md). Processus :
[`docs/ai_workflow/workflow.md`](docs/ai_workflow/workflow.md).

Branche `bl/XXX-description` depuis `version/vX.Y.Z`, commit `BL-XXX: action`,
PR verte (qualité + tests ≥ 95 % + build).

## Licence

Distribué sous licence **MIT**. Voir [`LICENSE`](LICENSE).
