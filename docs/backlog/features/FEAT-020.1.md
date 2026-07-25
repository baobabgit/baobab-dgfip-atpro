# FEAT-020.1 - Persistance appels et segments

Projet : AT Pro Pilotage  
Version cible : `v0.2.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Enregistrer les appels globaux et leurs segments sans perdre la structure multi-lignes produite par les parseurs.

### Perimetre

Inclut :

- repository `Call` ;
- repository `CallSegment` ;
- lien vers l'agent si reconnu ;
- lien vers le lot d'import ;
- empreinte de ligne ou de segment ;
- contrainte d'unicite sur l'appel source ;
- contrainte d'unicite sur les segments.

Exclut :

- calculs statistiques ;
- rapprochement appels-tickets ;
- interpretation avancee de performance.

### Exigences

- Ne jamais dedupliquer un appel en supprimant ses segments.
- Un appel identique reimporte doit etre ignore proprement.
- Un segment identique reimporte doit etre ignore proprement.
- Un appel existant avec contenu different doit remonter un conflit exploitable.
- Les timestamps d'appel doivent conserver le fuseau ou la regle de conversion documentee.

### Livrables attendus

```text
src/atpro/infrastructure/database/repositories/call_repository.py
src/atpro/infrastructure/database/repositories/call_segment_repository.py
tests/infrastructure/database/repositories/test_call_repository.py
```

### Tests

- Appel sans segment refuse si le modele l'interdit.
- Appel multi-segments conserve.
- Reimport identique sans doublon.
- Conflit de contenu detecte.

### Acceptation

- Les appels entrants et sortants v0.1.0 peuvent etre persistés dans le meme modele relationnel.

### References

- US-020
