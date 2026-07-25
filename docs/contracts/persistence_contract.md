# Contrat de persistance AT Pro Pilotage

Version cible : `v0.2.0`

## Role

Le contrat de persistance decrit comment les modeles canoniques produits par le parseur sont enregistres dans PostgreSQL.

La persistance n'est pas responsable de lire les CSV, de calculer les statistiques, de generer les rapports ou d'exposer une API HTTP.

## Principes

- Les cas d'usage applicatifs passent par une Unit of Work.
- Les repositories recoivent des objets domaine ou commandes applicatives, jamais des lignes CSV brutes.
- Les contraintes PostgreSQL protegent les cles metier.
- Les imports sont idempotents.
- Chaque donnee importee conserve une provenance.
- Les donnees sensibles sont limitees, masquees ou hachees selon leur usage.

## Entrees principales

- `ParseResult` produit par le parseur v0.1.0.
- `ImportedFileMetadata`.
- `Call` et `CallSegment`.
- `Ticket`.
- `AgentDailyActivity`.
- `Agent`, `Site`, `AgentAlias`, `AgentSiteAssignment`.

## Sorties principales

- `ImportBatch`.
- Compteurs d'import : inserted, ignored, updated, rejected, conflicted.
- `ImportRejectedRow`.
- Diagnostics de conflit.
- Statut de rollback.

## Idempotence

Un import identique ne doit creer aucune ligne metier supplementaire.

Les protections minimales sont :

- SHA-256 du fichier ;
- cles metier uniques ;
- empreintes normalisees de contenu ;
- transaction unique ;
- gestion explicite des conflits.

## Rollback

Le rollback d'un lot doit etre transactionnel.

Le lot et ses diagnostics restent auditables apres annulation.

## Exceptions

Les erreurs techniques SQLAlchemy restent dans l'infrastructure.

Les cas d'usage exposent des erreurs applicatives lisibles par le CLI et la future API.
