# FEAT-018.2 - Repositories alias et affectations

Projet : AT Pro Pilotage  
Version cible : `v0.2.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Gerer les variantes de noms agents et les rattachements dates entre agents et sites.

### Perimetre

Inclut :

- creation d'alias agent ;
- recherche d'un agent par alias normalise ;
- creation d'affectation agent-site ;
- detection de chevauchement d'affectations ;
- consultation de l'affectation applicable a une date.

Exclut :

- resolution interactive des ambiguities ;
- workflow de validation fonctionnelle ;
- permissions administrateur.

### Exigences

- Un alias normalise ne doit pas pointer vers deux agents actifs sans marquage ambigu.
- Les affectations doivent supporter une date de fin nulle.
- Le chevauchement d'affectations pour un meme agent doit etre refuse ou explicitement signale.
- Les imports doivent pouvoir creer des alias candidats non valides si la strategie le prevoit.

### Livrables attendus

```text
src/atpro/infrastructure/database/repositories/agent_alias_repository.py
src/atpro/infrastructure/database/repositories/assignment_repository.py
tests/infrastructure/database/repositories/
```

### Tests

- Alias unique.
- Alias deja connu.
- Alias ambigu.
- Affectation ouverte.
- Chevauchement refuse.

### Acceptation

- Un import peut retrouver l'agent canonique depuis un nom source.
- Un rattachement site peut etre determine pour une date donnee.

### References

- US-018
