Spécifications AT Pro Pilotage (v0.1.0)
=======================================

Cette section porte le **cahier des charges** (entrée humaine figée) pour le
projet **AT Pro Pilotage**, version cible ``v0.1.0``.

Les **User Stories**, **Features** et **Backlogs de livraison** ne sont **pas**
dupliqués ici : leur emplacement canonique AGENTS-compatible est
``docs/backlog/``.

Emplacements
------------

==========================================  ========================================
Contenu                                     Chemin
==========================================  ========================================
Cahier des charges                          ``000_cahier-des-charges/``
User Stories (``US-XXX``)                   ``docs/backlog/user_stories/``
Features (``FEAT-XXX.Y``)                   ``docs/backlog/features/``
Backlogs (``BL-XXX``)                       ``docs/backlog/backlogs/``
Index / matrice de traçabilité              ``docs/backlog/index.rst``
CSV de référence                            ``docs/reference-data.md``
File d'exécution                            ``docs/ai_workflow/state/queue.yaml``
==========================================  ========================================

Ordre de lecture recommandé
---------------------------

1. ``000_cahier-des-charges/``
2. ``docs/backlog/user_stories/``
3. ``docs/backlog/features/``
4. ``docs/backlog/backlogs/``
5. ``docs/reference-data.md``
6. ``docs/ai_workflow/state/queue.yaml``
7. ``docs/architecture/adr/``

Résumé du lot v0.1.0
--------------------

La version ``v0.1.0`` livre le cœur Python de parsing du package ``atpro`` :
ADR de cadrage, modèles métier, détection / normalisation, parseurs CSV,
``ParseResult``, CLI ``file``, fixtures anonymisées, cadrage des CSV réels de
référence, contrats publics et matrice de compatibilité.

Hors périmètre : PostgreSQL, FastAPI, React, Docker applicatif complet,
statistiques, Quarkdown, authentification, rapprochement appels / tickets.

Hiérarchie et identifiants
--------------------------

=====================  ===========================  =============================
Niveau                 Identifiant                  Emplacement
=====================  ===========================  =============================
User Story             ``US-001`` … ``US-013``      ``docs/backlog/user_stories/``
Feature                ``FEAT-XXX.Y``               ``docs/backlog/features/``
Backlog de livraison   ``BL-001`` … ``BL-021``      ``docs/backlog/backlogs/``
=====================  ===========================  =============================

Ces identifiants sont propagés dans les commits, les noms de tests et les
docstrings (champ ``:spec:``).

Premier item exécutable : ``BL-001`` (voir ``docs/backlog/index.rst`` pour la
matrice US / FEAT / BL).

.. toctree::
   :maxdepth: 1

   glossary
