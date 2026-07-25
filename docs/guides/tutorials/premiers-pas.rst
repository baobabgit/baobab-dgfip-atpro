Premiers pas avec atpro
=======================

Ce tutoriel installe le package ``atpro`` (v0.1.0) et vérifie le parseur CSV
via le CLI et les tests.

Prérequis
---------

* Python 3.13
* `uv <https://docs.astral.sh/uv/>`_

Installation
------------

::

   git clone https://github.com/baobabgit/baobab-dgfip-atpro.git
   cd baobab-dgfip-atpro
   make install

Sous Windows sans ``make`` ::

   uv sync
   uv run pre-commit install

Vérifier le CLI
---------------

::

   uv run atpro file inspect tests/fixtures/csv/incoming_calls_valid.csv
   uv run atpro file validate tests/fixtures/csv/incoming_calls_valid.csv --json
   uv run atpro file preview tests/fixtures/csv/incoming_calls_valid.csv --limit 5

API Python minimale
-------------------

::

   from pathlib import Path
   from atpro.parser import ParseFileUseCase

   result = ParseFileUseCase().parse(Path("tests/fixtures/csv/incoming_calls_valid.csv"))
   print(result.summary.status)

Qualité
-------

::

   make all

Ou ::

   uv run black --check src tests
   uv run ruff check src tests
   uv run mypy src
   uv run pytest -q --cov=src --cov-fail-under=95

La couverture doit rester ≥ 95 %.

Suite
-----

* CLI détaillé : ``docs/guides/how-to/cli-file.rst``
* Périmètre / limites : ``docs/guides/how-to/perimetre-v010.rst``
* Contrats : ``docs/contracts/``
