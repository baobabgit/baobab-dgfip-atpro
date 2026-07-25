# Context — BL-025

Apres ADR-0002, la configuration PostgreSQL (BL-023) et Compose (BL-024),
fournir l'infrastructure SQLAlchemy 2.x minimale :

- base declarative avec conventions de nommage ;
- fabrique d'engine depuis `DatabaseSettings` ;
- fabrique de sessions injectables (pas de session globale mutable) ;
- aucun effet reseau a l'import des modules.

Hors perimetre : UoW (BL-026), Alembic (BL-027), modeles ORM metier.
