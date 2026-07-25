# Release report v0.2.0

Statut : `PLANNED`

## Objectif

La v0.2.0 doit transformer le moteur de parsing v0.1.0 en socle persistant : donnees en PostgreSQL, imports idempotents, provenance, conflits visibles, rollback controle et exploitation CLI.

## Backlogs inclus

- BL-022 a BL-047.

## Criteres de release

- ADR-0002 validee.
- PostgreSQL Docker operationnel.
- Alembic `upgrade head` valide.
- Repositories principaux testes.
- Import transactionnel teste.
- Idempotence prouvee par test d'integration.
- Rollback prouve par test d'integration.
- CLI imports et referentiels operationnel.
- Documentation et contrats mis a jour.
- Traceabilite OK.

## Points de vigilance

- Ne pas commencer les statistiques v0.3.0 dans ce lot.
- Ne pas introduire FastAPI ou React avant les versions prevues.
- Ne pas stocker de donnees personnelles non utiles.
- Garder la base PostgreSQL comme derniere protection contre les doublons.

## Decision de passage en release

A renseigner en fin de developpement.
