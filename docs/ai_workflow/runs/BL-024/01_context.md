# Context — BL-024

Fournir une base PostgreSQL 17 locale reproductible pour migrations, imports et
tests d'integration, sans installer Postgres sur l'hote.

Perimetre : service `postgres` seul (pas backend / frontend / Nginx / worker).
Credentials de developpement uniquement ; documentation demarrage / arret /
nettoyage du volume.
