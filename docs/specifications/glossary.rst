Glossaire
=========

.. glossary::

   AT Pro Pilotage
      Projet cible de cette librairie : ingestion et parsing des fichiers CSV
      d'activité téléphonique (appels, tickets, activités agents) pour le
      pilotage AT Pro. Version initiale ``v0.1.0``.

   US
      *User Story*. Expression d'un besoin du point de vue de l'utilisateur
      (ou de l'IA de développement). Identifiants ``US-001`` à ``US-013`` pour
      ``v0.1.0``, fichiers dans ``docs/backlog/user_stories/``.

   FEAT
      *Feature*. Fonctionnalité concrète découpant une ou plusieurs US.
      Identifiants ``FEAT-XXX.Y`` (ex. ``FEAT-001.1``), fichiers dans
      ``docs/backlog/features/``.

   BL
      *Backlog de livraison*. Item d'implémentation atomique dérivé des FEAT.
      Identifiants ``BL-001`` à ``BL-021`` pour ``v0.1.0``, fichiers dans
      ``docs/backlog/backlogs/``. File d'exécution :
      ``docs/ai_workflow/state/queue.yaml``.

   ADR
      *Architecture Decision Record*. Décision d'architecture structurante,
      déposée dans ``docs/architecture/adr/`` (voir ADR-0001 pour la structure
      du dépôt ``v0.1.0``).

   atpro
      Nom du package Python livré en ``v0.1.0``. Cœur de parsing CSV, sans
      persistence ni API web dans ce lot.

   ParseResult
      Résultat standardisé d'un parsing : enregistrements, erreurs, warnings et
      résumé (summary). Produit par l'orchestrateur.

   Reader
      Composant qui lit et mappe un type de fichier CSV vers les modèles métier
      (appels entrants, appels sortants, tickets, activités agents).

   Normalizer
      Composant qui normalise textes, dates, durées, pourcentages, identités
      agents et sites avant ou pendant le parsing.

   Orchestrateur
      Service qui enchaîne détection, normalisation, lecture et assemblage du
      ``ParseResult``. Le CLI ne fait qu'appeler cet orchestrateur.

   Schéma
      Description attendue des colonnes / type de fichier CSV, gérée via un
      registre de schémas et une détection de type.

   Fixture
      Jeu de données de test anonymisé couvrant les formats CSV du lot, sans
      données sensibles (US-012 / FEAT-012.1). Suffisant pour la CI.

   CSV de référence
      Fichiers CSV réels optionnels pour validation locale. Fournis via
      ``ATPRO_REFERENCE_CSV_DIR`` (voir ``docs/reference-data.md`` et US-013).
      Jamais versionnés s'ils contiennent des données sensibles.

   CLI file
      Interface en ligne de commande minimale du lot ``v0.1.0`` :
      ``atpro file inspect``, ``atpro file validate``, ``atpro file preview``.

   Appels entrants
      Fichier CSV d'appels reçus ; peut contenir des enregistrements multi-lignes
      à consolider (US-005 / FEAT-005.4).

   Appels sortants
      Fichier CSV d'appels émis (US-006 / FEAT-006.1).

   Tickets
      Fichier CSV de tickets associés à l'activité (US-007 / FEAT-007.1).

   Activités agents
      Fichiers CSV d'activité des agents, en **format large** (US-008) ou
      **format long** (US-009).

   Backlog
      Ensemble des items BL à réaliser pour livrer la version. Source unique :
      ``docs/backlog/`` ; suivi via ``queue.yaml`` et ``dependency_graph.yaml``.

   Sprint
      Itération de durée fixe (champ *Iteration* du Project) regroupant des
      tâches, lorsque le suivi GitHub Projects est utilisé.
