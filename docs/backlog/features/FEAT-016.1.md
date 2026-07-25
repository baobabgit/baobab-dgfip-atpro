# FEAT-016.1 - Engine et sessions SQLAlchemy

Projet : AT Pro Pilotage  
Version cible : `v0.2.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Mettre en place l'infrastructure SQLAlchemy minimale, stable et typable pour acceder a PostgreSQL.

### Perimetre

Inclut :

- creation de l'engine ;
- fabrique de sessions ;
- base declarative ;
- conventions de nommage des contraintes ;
- helper de session pour le CLI et les tests.

Exclut :

- modeles ORM complets si la migration initiale n'est pas encore livree ;
- pooling avance production ;
- acces asynchrone.

### Exigences

- Utiliser SQLAlchemy 2.x.
- Le code doit respecter le typage strict du depot.
- Les sessions ne doivent pas etre globales et mutables.
- Les transactions sont controlees par la Unit of Work.
- Les erreurs techniques doivent rester separees des erreurs metier.

### Livrables attendus

```text
src/atpro/infrastructure/database/base.py
src/atpro/infrastructure/database/session.py
tests/infrastructure/database/test_session.py
```

### Tests

- Creation d'engine avec URL valide.
- Creation et fermeture de session.
- Rollback sur exception.
- Import des modules sans effet de bord reseau.

### Acceptation

- Les repositories peuvent recevoir une session injectee.
- Le code ne cree pas de connexion pendant l'import Python des modules.

### References

- US-016
