# FEAT-001.1 - Structure du depot et ADR de cadrage

Projet : AT Pro Pilotage  
Version cible : `v0.1.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Reconcilier le workflow existant du depot avec la cible applicative.

### Perimetre

Inclut :

- lecture de `AGENTS.md` ;
- verification du squelette existant ;
- choix documente entre `src/atpro` racine et future structure `backend/src/atpro` ;
- nettoyage du template ;
- initialisation des dossiers de documentation ;
- creation d'une ADR.

Exclut :

- creation de `frontend/` ;
- creation de `compose.yml` applicatif complet ;
- migrations base de donnees.

### Exigences

- Le package Python doit s'appeler `atpro`.
- La structure doit respecter les regles du depot.
- Si `AGENTS.md` impose le mono-package, `src/atpro` est la structure par defaut.
- La transition future vers application dockerisee doit etre documentee.
- Le seuil de couverture global du depot prevaut.

### Fichiers attendus

```text
docs/architecture/adr/ADR-0001-structure-depot-v010.md
src/atpro/
tests/
docs/backlog/
```

### Tests

- Import du package `atpro`.
- Commande de validation Python existante ou documentee.

### Acceptation

- `example_package` n'est plus le package applicatif.
- L'ADR explique clairement le choix de structure.



### References

- US-001
