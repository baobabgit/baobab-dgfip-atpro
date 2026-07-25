# FEAT-019.1 - Lots d'import et provenance

Projet : AT Pro Pilotage  
Version cible : `v0.2.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Tracer chaque import, son fichier source, son empreinte, son statut et les lignes rejetees.

### Perimetre

Inclut :

- table et repository `ImportBatch` ;
- table et repository `ImportRejectedRow` ;
- empreinte SHA-256 du fichier ;
- type et version de schema detectes ;
- periode couverte ;
- compteurs acceptes, ignores, rejetes ;
- statut d'import.

Exclut :

- stockage du fichier brut complet ;
- interface Web d'historique ;
- purge automatique.

### Exigences

- Un fichier strictement identique ne doit pas etre importe deux fois.
- Les lignes rejetees doivent masquer les donnees sensibles.
- Les statuts doivent permettre `analyzed`, `imported`, `partially_rejected`, `failed`, `rolled_back`.
- La provenance doit etre liee aux donnees metier importees.

### Livrables attendus

```text
src/atpro/domain/imports/
src/atpro/infrastructure/database/repositories/import_batch_repository.py
src/atpro/infrastructure/database/repositories/rejected_row_repository.py
```

### Tests

- Creation de lot.
- Refus ou signalement d'un SHA-256 deja importe.
- Enregistrement de lignes rejetees.
- Mise a jour de statut.

### Acceptation

- Chaque donnee metier importee peut etre rattachee a un lot.
- L'historique d'import est exploitable par le CLI.

### References

- US-019
