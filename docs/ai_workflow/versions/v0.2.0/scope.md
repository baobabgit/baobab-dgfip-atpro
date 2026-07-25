# Perimetre v0.2.0

## Objectif

Enregistrer les modeles normalises issus du parseur v0.1.0 dans PostgreSQL, sans doublon, avec provenance, diagnostics d'import, rollback controle et commandes CLI minimales.

## Inclus

- ADR `ADR-0002-persistance-postgresql-v020.md`.
- PostgreSQL via Docker Compose de developpement.
- Configuration base de donnees centralisee.
- SQLAlchemy 2.x.
- Unit of Work transactionnelle.
- Alembic et migrations initiales.
- Tables referentiels : sites, agents, alias, affectations.
- Tables imports : lots d'import, lignes rejetees.
- Tables metier : appels, segments, tickets, activites journalieres agents.
- Repositories applicatifs et implementations SQLAlchemy.
- Empreintes SHA-256 fichier et empreintes normalisees de donnees.
- Import transactionnel depuis `ParseResult`.
- Politique conservative de conflits.
- Quarantaine des lignes rejetees avec masquage.
- Rollback controle d'un lot d'import.
- CLI imports et referentiels.
- Tests d'integration PostgreSQL.
- Contrats et documentation d'exploitation.

## Exclus

- Statistiques site et agent.
- API FastAPI.
- Interface React.
- Worker asynchrone.
- Rapports Quarkdown.
- Authentification et roles.
- Production Docker complete.

## Hypotheses

- La structure de depot reste `src/atpro` jusqu'a nouvelle ADR.
- Les fichiers CSV reels de reference sont cadres par BL-021.
- Le fuseau horaire applicatif par defaut est `Europe/Paris` pour les donnees horaires sans timezone explicite.
- Les imports v0.2.0 utilisent une politique globale de conflit, extensible plus tard.

## Risques

- Concurrence d'import sur les memes cles metier.
- Ambiguite des agents sans referentiel assez riche.
- Rollback complexe si une meme donnee est rattachee a plusieurs lots.
- Divergence entre modeles domaine v0.1.0 et schema relationnel si les migrations sont faites trop tot.
