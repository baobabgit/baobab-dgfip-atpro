# FEAT-024.1 - Politique de conflits et mises a jour

Projet : AT Pro Pilotage  
Version cible : `v0.2.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Definir et implementer la conduite a tenir lorsqu'une cle metier existe deja avec un contenu different.

### Perimetre

Inclut :

- politique globale par defaut ;
- comportement par famille de donnees ;
- journalisation des differences ;
- retour applicatif clair ;
- documentation des options futures.

Exclut :

- ecran Web de resolution ;
- workflow multi-validateur ;
- versionnement complet ligne par ligne.

### Exigences

- La politique par defaut doit etre conservative.
- Pour `AgentDailyActivity`, le niveau de configuration doit etre explicite : global en v0.2.0, extensible par import plus tard.
- Les tickets modifies doivent etre identifies sans ecraser silencieusement des champs.
- Les conflits bloquants doivent laisser le lot dans un statut comprehensible.

### Livrables attendus

```text
src/atpro/application/imports/conflict_policy.py
src/atpro/domain/imports/import_conflict.py
docs/operations/imports.md
```

### Tests

- Politique `ignore_existing`.
- Politique `fail_on_change`.
- Politique `update_if_newer` si retenue.
- Differences masquees pour donnees sensibles.

### Acceptation

- Une IA de developpement sait exactement quoi faire pour chaque conflit de v0.2.0.

### References

- US-024
