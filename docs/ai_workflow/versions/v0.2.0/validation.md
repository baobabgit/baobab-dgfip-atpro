# Validation v0.2.0

## Criteres de sortie

- PostgreSQL demarre via Docker Compose.
- Alembic applique le schema sur une base vide.
- Les repositories agents, sites, alias et affectations sont operationnels.
- Les repositories imports, appels, tickets et activites sont operationnels.
- Un meme fichier importe deux fois ne cree pas de doublon metier.
- Un import partiellement chevauchant n'ajoute que les donnees nouvelles.
- Un conflit de contenu est detecte et rapporte.
- Les lignes rejetees sont conservees avec donnees sensibles masquees.
- Un lot d'import peut etre annule de facon controlee.
- Les commandes CLI d'import et de referentiels fonctionnent.
- Les tests PostgreSQL sont documentes et sans warning pytest non declare.
- Les contrats publics ne contiennent aucune reference au template.
- `python scripts/check_traceability.py` passe.

## Tests attendus

- Tests unitaires configuration DB.
- Tests unitaires Unit of Work.
- Tests repositories sur PostgreSQL.
- Tests applicatifs import transactionnel.
- Tests idempotence.
- Tests rollback.
- Tests CLI.
- Tests de documentation/traceabilite.

## Donnees de test

- Fixtures anonymisees v0.1.0.
- Fichiers de reference reels si disponibles selon BL-021.
- Jeux minimaux construits en test pour chaque famille de donnees.

## Non valide en v0.2.0

- Performance sur gros volumes.
- Calculs statistiques.
- Consultation Web.
- Securisation finale des roles.
