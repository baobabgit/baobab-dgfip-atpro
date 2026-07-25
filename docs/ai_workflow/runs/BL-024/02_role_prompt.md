# Role prompt — Developpeur Python

Livrer Compose + documentation selon BL-024 / FEAT-015.1.

- PostgreSQL 17, volume persistant, healthcheck `pg_isready` ;
- port configurable via variables d'environnement ;
- aucun secret de production dans le depot ;
- documenter demarrage, arret, nettoyage et diagnostic ;
- tests structurels du compose / de la doc (demarrage Docker optionnel hors CI).
