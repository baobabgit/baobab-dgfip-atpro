# FEAT-018.1 - Repositories agents et sites

Projet : AT Pro Pilotage  
Version cible : `v0.2.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Persister et consulter les referentiels `Agent` et `Site` via des ports applicatifs independants de SQLAlchemy.

### Perimetre

Inclut :

- creation de sites ;
- creation d'agents ;
- recherche par identifiant interne ;
- recherche par nom canonique ;
- liste paginee ou bornee pour le CLI ;
- idempotence sur les cles metier.

Exclut :

- interface Web de gestion ;
- permissions ;
- historisation fine de toutes les modifications administratives.

### Exigences

- Les repositories ne doivent pas accepter d'objets ORM en entree applicative.
- Les noms doivent etre normalises selon les normalizers v0.1.0.
- Les doublons doivent etre geres par contrainte SQL et retour explicite.
- Les agents et sites inactifs restent consultables.

### Livrables attendus

```text
src/atpro/application/ports/repositories.py
src/atpro/infrastructure/database/repositories/agent_repository.py
src/atpro/infrastructure/database/repositories/site_repository.py
tests/infrastructure/database/repositories/
```

### Tests

- Insertion nouvelle.
- Reimport identique sans doublon.
- Recherche par cle.
- Gestion d'un conflit de nom.

### Acceptation

- Les cas d'usage v0.2.0 peuvent rattacher des donnees a des agents et sites persistants.

### References

- US-018
