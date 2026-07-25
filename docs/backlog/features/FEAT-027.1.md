# FEAT-027.1 - Commandes CLI d'import

Projet : AT Pro Pilotage  
Version cible : `v0.2.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Exposer l'import PostgreSQL v0.2.0 par le CLI en reutilisant les cas d'usage applicatifs.

### Perimetre

Inclut :

- `atpro import run` ;
- `atpro import list` ;
- `atpro import show` ;
- `atpro import errors` ;
- `atpro import rollback` ;
- options de sortie humaine et JSON si le CLI v0.1.0 les supporte.

Exclut :

- API HTTP ;
- worker asynchrone ;
- planification.

### Exigences

- Le CLI ne doit contenir ni SQL ni logique de parsing metier.
- Les erreurs doivent produire un code retour coherent.
- Les commandes destructives ou sensibles doivent afficher clairement leur cible.
- Le chemin fichier ou dossier doit etre valide avant import.

### Livrables attendus

```text
src/atpro/interfaces/cli/import_commands.py
tests/interfaces/cli/test_import_commands.py
```

### Tests

- Import fichier.
- Import dossier.
- Liste des lots.
- Affichage des erreurs.
- Rollback.

### Acceptation

- Un utilisateur technique peut importer, verifier et annuler un lot depuis le terminal.

### References

- US-027
