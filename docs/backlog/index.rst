Backlog AT Pro Pilotage v0.1.0 et v0.2.0
=========================================

Ce dossier est la **source unique** AGENTS-compatible pour les lots ``v0.1.0``
et ``v0.2.0`` (US, FEAT et BL).

Structure
---------

===================  =======================  ==================
Dossier              Contenu                  Convention
===================  =======================  ==================
``user_stories/``    28 user stories          ``US-XXX.md``
``features/``        41 features              ``FEAT-XXX.Y.md``
``backlogs/``        47 items de backlog      ``BL-XXX.md``
===================  =======================  ==================

User stories
------------

Fichier         Titre
==============  ========================================================================
``US-001.md``   Initialiser le socle de developpement v0.1.0
``US-002.md``   Inspecter un fichier CSV
``US-003.md``   Valider un fichier CSV
``US-004.md``   Previsualiser un fichier CSV parse
``US-005.md``   Parser un fichier d'appels entrants
``US-006.md``   Parser un fichier d'appels sortants
``US-007.md``   Parser un fichier tickets
``US-008.md``   Parser un fichier activites agents format large
``US-009.md``   Parser un fichier activites agents format long
``US-010.md``   Normaliser les identites agents et sites
``US-011.md``   Produire un resultat de parsing standardise
``US-012.md``   Construire des fixtures de test anonymisees
``US-013.md``   Definir et verifier la fourniture des CSV de reference reels
``US-014.md``   Cadrer l'architecture de persistance v0.2.0
``US-015.md``   Lancer PostgreSQL en environnement de developpement
``US-016.md``   Configurer SQLAlchemy, sessions et Unit of Work
``US-017.md``   Creer le schema PostgreSQL avec Alembic
``US-018.md``   Persister les referentiels agents, sites, alias et affectations
``US-019.md``   Tracer les lots d'import et les lignes rejetees
``US-020.md``   Persister les appels et segments d'appels
``US-021.md``   Persister les tickets
``US-022.md``   Persister les activites journalieres agents
``US-023.md``   Executer un import transactionnel depuis ParseResult
``US-024.md``   Gerer les conflits et politiques de mise a jour
``US-025.md``   Mettre en quarantaine les lignes rejetees
``US-026.md``   Annuler un lot d'import
``US-027.md``   Exploiter imports et referentiels via CLI
``US-028.md``   Tester l'integration PostgreSQL et documenter v0.2.0
==============  ========================================================================

Features
--------

Fichier           Titre
================  ========================================================================
``FEAT-001.1.md``  Structure du depot et ADR de cadrage
``FEAT-001.2.md``  Documentation developpeur v0.1.0
``FEAT-002.1.md``  Metadonnees fichier et empreinte SHA-256
``FEAT-002.2.md``  Detection encodage, separateur et en-tetes
``FEAT-002.3.md``  Registre de schemas et detection du type de fichier
``FEAT-002.4.md``  Orchestrateur de parsing
``FEAT-002.5.md``  CLI minimal `file`
``FEAT-003.1.md``  Validation, erreurs et avertissements
``FEAT-005.1.md``  Modeles metier canoniques
``FEAT-005.2.md``  Enumerations et value objects
``FEAT-005.3.md``  Normalisation texte, dates, durees et pourcentages
``FEAT-005.4.md``  Reader appels entrants
``FEAT-006.1.md``  Reader appels sortants
``FEAT-007.1.md``  Reader tickets
``FEAT-008.1.md``  Reader activites agents format large
``FEAT-009.1.md``  Reader activites agents format long
``FEAT-010.1.md``  Normalisation agents et sites
``FEAT-012.1.md``  Fixtures anonymisees et donnees de test
``FEAT-013.1.md``  Modalite des CSV de reference et tests optionnels
``FEAT-014.1.md``  ADR de persistance v0.2.0
``FEAT-015.1.md``  PostgreSQL Docker de developpement
``FEAT-015.2.md``  Configuration base de donnees
``FEAT-016.1.md``  Engine et sessions SQLAlchemy
``FEAT-016.2.md``  Unit of Work transactionnelle
``FEAT-017.1.md``  Initialisation Alembic
``FEAT-017.2.md``  Schema relationnel v0.2.0
``FEAT-018.1.md``  Repositories agents et sites
``FEAT-018.2.md``  Repositories alias et affectations
``FEAT-019.1.md``  Lots d'import et provenance
``FEAT-020.1.md``  Persistance appels et segments
``FEAT-021.1.md``  Persistance tickets
``FEAT-022.1.md``  Persistance activites journalieres agents
``FEAT-023.1.md``  Cas d'usage d'import transactionnel
``FEAT-023.2.md``  Idempotence et empreintes normalisees
``FEAT-024.1.md``  Politique de conflits et mises a jour
``FEAT-025.1.md``  Quarantaine des lignes rejetees
``FEAT-026.1.md``  Annulation controlee d'un import
``FEAT-027.1.md``  Commandes CLI d'import
``FEAT-027.2.md``  Commandes CLI referentiels
``FEAT-028.1.md``  Tests d'integration PostgreSQL
``FEAT-028.2.md``  Documentation, contrats et release v0.2.0
================  ========================================================================

Backlog
-------

Fichier         Titre
==============  ========================================================================
``BL-001.md``   Lire le contexte et ouvrir l'ADR depot
``BL-002.md``   Nettoyer le squelette template
``BL-003.md``   Initialiser l'arborescence du domaine
``BL-004.md``   Implementer enums et value objects
``BL-005.md``   Implementer les modeles metier
``BL-006.md``   Implementer erreurs, warnings et resultats
``BL-007.md``   Implementer detection fichier
``BL-008.md``   Implementer registre de schemas
``BL-009.md``   Implementer normalizers generiques
``BL-010.md``   Implementer normalizers agents et sites
``BL-011.md``   Implementer reader appels commun
``BL-012.md``   Implementer reader appels entrants
``BL-013.md``   Implementer reader appels sortants
``BL-014.md``   Implementer reader tickets
``BL-015.md``   Implementer readers activites agents
``BL-016.md``   Implementer orchestrateur de parsing
``BL-017.md``   Implementer CLI minimal
``BL-018.md``   Creer fixtures anonymisees
``BL-019.md``   Couvrir les tests de non-regression parseurs
``BL-020.md``   Documenter le lot v0.1.0
``BL-021.md``   Cadrer et cabler les fichiers CSV reels de reference
``BL-022.md``   Rediger l'ADR de persistance v0.2.0
``BL-023.md``   Ajouter dependances et configuration PostgreSQL
``BL-024.md``   Fournir PostgreSQL via Docker Compose
``BL-025.md``   Implementer engine et sessions SQLAlchemy
``BL-026.md``   Implementer la Unit of Work SQLAlchemy
``BL-027.md``   Initialiser Alembic
``BL-028.md``   Migrer les tables imports et referentiels
``BL-029.md``   Migrer les tables metier importees
``BL-030.md``   Implementer repositories Site et Agent
``BL-031.md``   Implementer repositories Alias et Affectation
``BL-032.md``   Implementer repositories ImportBatch et RejectedRow
``BL-033.md``   Implementer repositories Call et CallSegment
``BL-034.md``   Implementer repository Ticket
``BL-035.md``   Implementer repository AgentDailyActivity
``BL-036.md``   Implementer empreintes et detection de doublons
``BL-037.md``   Implementer le cas d'usage ImportParsedFile
``BL-038.md``   Implementer la politique de conflit
``BL-039.md``   Implementer la quarantaine des lignes rejetees
``BL-040.md``   Implementer l'annulation d'un lot d'import
``BL-041.md``   Ajouter les commandes CLI import
``BL-042.md``   Ajouter les commandes CLI referentiels
``BL-043.md``   Mettre en place les tests d'integration PostgreSQL
``BL-044.md``   Couvrir l'idempotence par tests d'integration
``BL-045.md``   Couvrir le rollback par tests d'integration
``BL-046.md``   Mettre a jour contrats et documentation v0.2.0
``BL-047.md``   Finaliser workflow et release report v0.2.0
==============  ========================================================================

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
US-014   FEAT-014.1                                               BL-022
US-015   FEAT-015.1, FEAT-015.2                                   BL-023, BL-024
US-016   FEAT-016.1, FEAT-016.2                                   BL-025, BL-026
US-017   FEAT-017.1, FEAT-017.2                                   BL-027, BL-028, BL-029
US-018   FEAT-018.1, FEAT-018.2                                   BL-030, BL-031
US-019   FEAT-019.1, FEAT-025.1                                   BL-032, BL-039
US-020   FEAT-020.1                                               BL-033
US-021   FEAT-021.1, FEAT-024.1                                   BL-034, BL-038
US-022   FEAT-022.1, FEAT-024.1                                   BL-035, BL-038
US-023   FEAT-023.1, FEAT-023.2                                   BL-036, BL-037, BL-044
US-024   FEAT-024.1                                               BL-038
US-025   FEAT-025.1                                               BL-039
US-026   FEAT-026.1                                               BL-040, BL-045
US-027   FEAT-027.1, FEAT-027.2                                   BL-041, BL-042
US-028   FEAT-028.1, FEAT-028.2                                   BL-043, BL-044, BL-045, BL-046, BL-047
=======  =======================================================  ===============================

Notes
-----

* Conventions AGENTS-compatible uniquement.
* ADR dans ``docs/architecture/adr/`` (ADR-0002 attendue pour ``v0.2.0``).
* Contrat de persistance : ``docs/contracts/persistence_contract.md``.
* File d'exécution : ``docs/ai_workflow/state/queue.yaml`` (premier item ``v0.2.0`` :
  ``BL-022``).
