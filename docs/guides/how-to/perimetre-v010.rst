Périmètre et limites v0.1.0
===========================

Objectif : savoir ce que livre le lot ``v0.1.0`` et ce qui reste hors scope
(FEAT-001.2).

Livré
-----

* Domaine : ``Site``, ``Agent``, ``Call``, ``CallSegment``, ``Ticket``,
  ``AgentDailyActivity``, alias et affectations.
* Parseur : détection, six schémas, readers, normalizers, ``ParseFileUseCase``,
  ``ParseResult`` / ``ParsePreview``.
* CLI : ``atpro file inspect|validate|preview``.
* Fixtures anonymisées + tests de non-régression.

Hors périmètre
--------------

* Base de données / persistence.
* API HTTP.
* Statistiques et indicateurs.
* Rapports (Quarkdown / PDF).
* Interface React.

Schémas et normalisation
------------------------

Détail dans ``docs/contracts/parser_contract.md`` :

* schémas ``incoming_calls_v1``, ``outgoing_calls_v1``, ``tickets_long``,
  ``tickets_reduced``, ``activities_wide``, ``activities_long`` ;
* dates en ``Europe/Paris``, durées, pourcentages, agents / sites, masquage
  email / téléphone.

Questions ouvertes
------------------

La liste complète (sites officiels, définitions d'appels / tickets, RGPD,
CSV de référence, etc.) est la **section 22** du cahier des charges :

``docs/specifications/000_cahier-des-charges/000_specifications.md``

Points encore structurants pour la suite après ``v0.1.0`` :

1. Liste officielle des sites et codes.
2. Règle de rattachement agent ↔ site sans affectation connue.
3. Emplacement et statut des CSV de référence réels (BL-021).
4. Fuseau horaire officiel et gestion des changements d'heure.
5. Politique de mise à jour des tickets / activités déjà importés
   (versions ultérieures avec persistence).

Matrice d'intégration
---------------------

``docs/integrations/compatibility_matrix.yaml`` — composants ``domain``,
``parser`` et ``cli`` en ``delivered`` ; ``database``, ``api``, ``frontend``
et ``reports`` en ``out_of_scope``.
