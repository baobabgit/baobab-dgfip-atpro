# Context — BL-023

Apres ADR-0002, preparer le package pour se connecter a PostgreSQL et executer
les migrations ulterieures :

- dependances SQLAlchemy 2.x, Alembic, driver `psycopg` ;
- configuration centralisee testable sans reseau ;
- masquage des mots de passe dans les representations ;
- `.env.example` sans secret reel ;
- marqueurs pytest `postgres` / `integration`.

Docker Compose (BL-024) et engine/sessions (BL-025) sont hors de ce BL.
