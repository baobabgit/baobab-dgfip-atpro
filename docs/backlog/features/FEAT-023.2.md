# FEAT-023.2 - Idempotence et empreintes normalisees

Projet : AT Pro Pilotage  
Version cible : `v0.2.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Garantir que les reimports identiques ou partiellement chevauchants ne produisent pas de doublons.

### Perimetre

Inclut :

- calcul d'empreinte fichier SHA-256 ;
- empreintes normalisees de donnees metier ;
- strategie `INSERT ... ON CONFLICT` ou equivalent SQLAlchemy ;
- statut `inserted`, `ignored`, `updated`, `conflict`;
- tests de reimport.

Exclut :

- reconciliation manuelle avancee ;
- merge interactif.

### Exigences

- L'empreinte normalisee ne doit pas dependre de l'ordre des colonnes CSV.
- Les valeurs vides equivalentes doivent etre normalisees de facon stable.
- La base reste l'autorite finale contre les doublons.
- Les compteurs doivent distinguer lignes ignorees et conflits.

### Livrables attendus

```text
src/atpro/application/imports/fingerprints.py
src/atpro/infrastructure/database/upsert.py
tests/application/imports/test_fingerprints.py
tests/integration/test_import_idempotence.py
```

### Tests

- Meme fichier importe deux fois.
- Deux fichiers differents contenant une meme donnee.
- Meme cle metier avec contenu different.
- Execution concurrente simulee si possible.

### Acceptation

- Le resultat d'un second import identique indique zero creation metier.

### References

- US-023
