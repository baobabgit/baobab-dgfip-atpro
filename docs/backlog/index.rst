Backlog AT Pro Pilotage v0.1.0
================================

Ce dossier est la **source unique** AGENTS-compatible pour le lot ``v0.1.0``
(US, FEAT et BL). Aucun miroir sous ``docs/specifications/``.

Structure
---------

===================  =======================  ==================
Dossier              Contenu                  Convention
===================  =======================  ==================
``user_stories/``    13 user stories          ``US-XXX.md``
``features/``        19 features              ``FEAT-XXX.Y.md``
``backlogs/``        21 items de backlog      ``BL-XXX.md``
===================  =======================  ==================

User stories
------------

===========  ==================================================================
Fichier      Titre
===========  ==================================================================
``US-001.md``  Initialiser le socle de développement v0.1.0
``US-002.md``  Inspecter un fichier CSV
``US-003.md``  Valider un fichier CSV
``US-004.md``  Prévisualiser un fichier CSV parsé
``US-005.md``  Parser un fichier d'appels entrants
``US-006.md``  Parser un fichier d'appels sortants
``US-007.md``  Parser un fichier tickets
``US-008.md``  Parser un fichier activités agents format large
``US-009.md``  Parser un fichier activités agents format long
``US-010.md``  Normaliser les identités agents et sites
``US-011.md``  Produire un résultat de parsing standardisé
``US-012.md``  Construire des fixtures de test anonymisées
``US-013.md``  Définir et vérifier la fourniture des CSV de référence réels
===========  ==================================================================

Features
--------

================  ===========================================================
Fichier           Titre
================  ===========================================================
``FEAT-001.1.md`` Structure du dépôt et ADR de cadrage
``FEAT-001.2.md`` Documentation développeur v0.1.0
``FEAT-002.1.md`` Métadonnées fichier et empreinte SHA-256
``FEAT-002.2.md`` Détection encodage, séparateur et en-têtes
``FEAT-002.3.md`` Registre de schémas et détection du type de fichier
``FEAT-002.4.md`` Orchestrateur de parsing
``FEAT-002.5.md`` CLI minimal ``file``
``FEAT-003.1.md`` Validation, erreurs et avertissements
``FEAT-005.1.md`` Modèles métier canoniques
``FEAT-005.2.md`` Énumérations et value objects
``FEAT-005.3.md`` Normalisation texte, dates, durées et pourcentages
``FEAT-005.4.md`` Reader appels entrants
``FEAT-006.1.md`` Reader appels sortants
``FEAT-007.1.md`` Reader tickets
``FEAT-008.1.md`` Reader activités agents format large
``FEAT-009.1.md`` Reader activités agents format long
``FEAT-010.1.md`` Normalisation agents et sites
``FEAT-012.1.md`` Fixtures anonymisées et données de test
``FEAT-013.1.md`` Modalité des CSV de référence et tests optionnels
================  ===========================================================

Backlog
-------

=============  ===========================================================
Fichier        Titre
=============  ===========================================================
``BL-001.md``  Lire le contexte et ouvrir l'ADR dépôt
``BL-002.md``  Nettoyer le squelette template
``BL-003.md``  Initialiser l'arborescence du domaine
``BL-004.md``  Implémenter enums et value objects
``BL-005.md``  Implémenter les modèles métier
``BL-006.md``  Implémenter erreurs, warnings et résultats
``BL-007.md``  Implémenter détection fichier
``BL-008.md``  Implémenter registre de schémas
``BL-009.md``  Implémenter normalizers génériques
``BL-010.md``  Implémenter normalizers agents et sites
``BL-011.md``  Implémenter reader appels commun
``BL-012.md``  Implémenter reader appels entrants
``BL-013.md``  Implémenter reader appels sortants
``BL-014.md``  Implémenter reader tickets
``BL-015.md``  Implémenter readers activités agents
``BL-016.md``  Implémenter orchestrateur de parsing
``BL-017.md``  Implémenter CLI minimal
``BL-018.md``  Créer fixtures anonymisées
``BL-019.md``  Couvrir les tests de non-régression parseurs
``BL-020.md``  Documenter le lot v0.1.0
``BL-021.md``  Cadrer et cabler les fichiers CSV réels de référence
=============  ===========================================================

Matrice de traçabilité
----------------------

=======  =======================================================  ===============================
US       FEAT                                                     BL
=======  =======================================================  ===============================
US-001   FEAT-001.1, FEAT-001.2                                   BL-001, BL-002, BL-003, BL-020
US-002   FEAT-002.1, FEAT-002.2, FEAT-002.3, FEAT-002.4, FEAT-002.5  BL-007, BL-008, BL-016, BL-017
US-003   FEAT-003.1                                               BL-006, BL-016, BL-017
US-004   FEAT-002.4, FEAT-002.5                                   BL-016, BL-017
US-005   FEAT-005.1, FEAT-005.2, FEAT-005.3, FEAT-005.4           BL-011, BL-012
US-006   FEAT-006.1                                               BL-011, BL-013
US-007   FEAT-007.1                                               BL-014
US-008   FEAT-008.1                                               BL-015
US-009   FEAT-009.1                                               BL-015
US-010   FEAT-010.1                                               BL-010
US-011   FEAT-003.1                                               BL-006, BL-016
US-012   FEAT-012.1                                               BL-018, BL-019
US-013   FEAT-013.1                                               BL-021
=======  =======================================================  ===============================

Notes
-----

* Les fiches utilisent uniquement les conventions AGENTS-compatible.
* Les ADR sont dans ``docs/architecture/adr/`` (ADR-0001 présente).
* CSV réels de référence : ``docs/reference-data.md``.
* File d'exécution : ``docs/ai_workflow/state/queue.yaml`` (premier item :
  ``BL-001``).
