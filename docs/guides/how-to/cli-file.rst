Utiliser le CLI ``atpro file``
==============================

Objectif : inspecter, valider ou prévisualiser un CSV AT Pro avec le CLI
livré en ``v0.1.0`` (FEAT-002.5).

Prérequis
---------

* Environnement installé (``make install`` ou ``uv sync``).
* Un fichier CSV (fixtures sous ``tests/fixtures/csv/`` pour les essais).

Commandes
---------

::

   uv run atpro file inspect <chemin.csv> [--json] [--verbose]
   uv run atpro file validate <chemin.csv> [--json] [--verbose]
   uv run atpro file preview <chemin.csv> [--limit N] [--json] [--verbose]

* ``--json`` : sortie structurée.
* ``--limit`` (preview seulement) : nombre max d'enregistrements (défaut ``10``).
* ``--verbose`` : détails supplémentaires (valeurs sensibles masquées).

Codes de sortie
---------------

=====  =========================  =================================
Code   Constante                  Signification
=====  =========================  =================================
0      SUCCESS                    Succès
1      INVALID_FILE               Fichier invalide
2      MISSING_OR_UNREADABLE      Introuvable, vide ou illisible
3      UNKNOWN_FORMAT             Format / schéma inconnu
4      TECHNICAL_ERROR            Erreur technique
=====  =========================  =================================

Vérification rapide
-------------------

::

   uv run atpro file inspect tests/fixtures/csv/incoming_calls_valid.csv
   uv run atpro file validate tests/fixtures/csv/incoming_calls_valid.csv --json
   echo %ERRORLEVEL%   # Windows — attendre 0

Références
----------

* Contrat : ``docs/contracts/cli_contract.md``
* Cas d'usage Python : ``ParseFileUseCase`` (``docs/contracts/public_api.md``)
