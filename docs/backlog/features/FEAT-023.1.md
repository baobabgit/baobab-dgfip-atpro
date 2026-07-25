# FEAT-023.1 - Cas d'usage d'import transactionnel

Projet : AT Pro Pilotage  
Version cible : `v0.2.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Transformer un `ParseResult` valide ou partiellement valide en ecritures PostgreSQL atomiques et tracables.

### Perimetre

Inclut :

- commande applicative `ImportParsedFileCommand` ;
- handler applicatif ;
- creation du lot d'import ;
- persistance des donnees metier ;
- persistance des lignes rejetees ;
- compteurs d'import ;
- commit unique.

Exclut :

- parsing lui-meme ;
- upload HTTP ;
- execution asynchrone worker.

### Exigences

- Si une erreur bloquante survient avant commit, aucune donnee ne reste en base.
- Les erreurs fonctionnelles doivent etre retournees sous forme de resultat exploitable.
- Le handler ne doit pas connaitre les details ORM.
- L'idempotence doit etre conservee meme en execution concurrente.

### Livrables attendus

```text
src/atpro/application/imports/import_parsed_file.py
tests/application/imports/test_import_parsed_file.py
```

### Tests

- Import complet.
- Import partiellement rejete.
- Import avec erreur bloquante.
- Rollback automatique.

### Acceptation

- Un flux parseur v0.1.0 vers PostgreSQL v0.2.0 fonctionne sans passer par le CLI.

### References

- US-023
