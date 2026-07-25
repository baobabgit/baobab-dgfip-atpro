# FEAT-027.2 - Commandes CLI referentiels

Projet : AT Pro Pilotage  
Version cible : `v0.2.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Permettre la gestion minimale des agents, sites, alias et affectations depuis le CLI.

### Perimetre

Inclut :

- `atpro agent list` ;
- `atpro agent show` ;
- `atpro agent add-alias` ;
- `atpro site list` ;
- `atpro site show` ;
- `atpro assignment add` ;
- sorties lisibles et exploitables.

Exclut :

- interface Web ;
- import massif de referentiel ;
- gestion de droits.

### Exigences

- Les commandes doivent appeler les services/repositories via la Unit of Work.
- Les identifiants affiches doivent permettre les commandes suivantes.
- Les dates d'affectation doivent etre validees.
- Les erreurs d'alias ambigu doivent etre comprehensibles.

### Livrables attendus

```text
src/atpro/interfaces/cli/referential_commands.py
tests/interfaces/cli/test_referential_commands.py
```

### Tests

- Liste agents/sites vide.
- Creation ou consultation selon commandes retenues.
- Ajout alias.
- Ajout affectation.
- Erreur date invalide.

### Acceptation

- Le referentiel necessaire aux imports peut etre prepare sans acces direct a PostgreSQL.

### References

- US-027
