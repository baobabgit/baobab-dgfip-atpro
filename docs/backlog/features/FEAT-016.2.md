# FEAT-016.2 - Unit of Work transactionnelle

Projet : AT Pro Pilotage  
Version cible : `v0.2.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Fournir un point d'entree transactionnel commun aux cas d'usage d'import, de rollback et de gestion des referentiels.

### Perimetre

Inclut :

- interface applicative de Unit of Work ;
- implementation SQLAlchemy ;
- exposition des repositories depuis la Unit of Work ;
- commit explicite ;
- rollback automatique en cas d'erreur.

Exclut :

- orchestration worker ;
- transactions distribuees ;
- gestion de concurrence avancee hors contraintes SQL.

### Exigences

- Les cas d'usage applicatifs ne doivent pas manipuler directement une session SQLAlchemy.
- La Unit of Work doit etre utilisable par le CLI et par la future API.
- Une exception avant commit ne doit laisser aucune ligne partiellement importee.
- Les tests doivent verifier commit et rollback.

### Livrables attendus

```text
src/atpro/application/ports/unit_of_work.py
src/atpro/infrastructure/database/unit_of_work.py
tests/infrastructure/database/test_unit_of_work.py
```

### Tests

- Commit persiste les donnees.
- Exception declenche rollback.
- Double commit ou reutilisation invalide est gere proprement.

### Acceptation

- Les imports v0.2.0 peuvent s'executer dans une transaction unique.
- La dependance SQLAlchemy reste dans `infrastructure`.

### References

- US-016
