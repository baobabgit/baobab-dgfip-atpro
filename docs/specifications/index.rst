Spécifications AT Pro Pilotage
==============================

Cette section porte le **cahier des charges** (entrée humaine figée) pour le
projet **AT Pro Pilotage**.

Les **User Stories**, **Features** et **Backlogs de livraison** sont dans
``docs/backlog/`` (source unique AGENTS-compatible).

Versions
--------

===========  ==============================================================
Version      Objet
===========  ==============================================================
``v0.1.0``   Package ``atpro``, parseurs CSV, CLI ``file`` (**RELEASED**)
``v0.2.0``   PostgreSQL, imports idempotents, CLI imports/référentiels
===========  ==============================================================

Emplacements
------------

==========================================  ========================================
Contenu                                     Chemin
==========================================  ========================================
Cahier des charges                          ``000_cahier-des-charges/``
User Stories / Features / Backlogs          ``docs/backlog/``
Index / matrice de traçabilité              ``docs/backlog/index.rst``
CSV de référence                            ``docs/reference-data.md``
Contrat de persistance                      ``docs/contracts/persistence_contract.md``
File d'exécution                            ``docs/ai_workflow/state/queue.yaml``
Version active                              ``docs/ai_workflow/versions/v0.2.0/``
==========================================  ========================================

Ordre de lecture recommandé
---------------------------

1. ``000_cahier-des-charges/``
2. ``docs/backlog/`` (US → FEAT → BL)
3. ``docs/contracts/`` (parser, CLI, persistance)
4. ``docs/ai_workflow/versions/v0.2.0/``
5. ``docs/ai_workflow/state/queue.yaml``

Hiérarchie et identifiants
--------------------------

=====================  ===========================  =============================
Niveau                 Identifiant                  Emplacement
=====================  ===========================  =============================
User Story             ``US-001`` … ``US-028``      ``docs/backlog/user_stories/``
Feature                ``FEAT-XXX.Y``               ``docs/backlog/features/``
Backlog de livraison   ``BL-001`` … ``BL-047``      ``docs/backlog/backlogs/``
=====================  ===========================  =============================

Premier item exécutable ``v0.2.0`` : ``BL-022`` (ADR persistance PostgreSQL).

.. toctree::
   :maxdepth: 1

   glossary
