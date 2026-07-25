# FEAT-014.1 - ADR de persistance v0.2.0

Projet : AT Pro Pilotage  
Version cible : `v0.2.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Cadrer la mise en place de la persistance PostgreSQL sans remettre en cause le choix `src/atpro` acte en `v0.1.0`.

### Perimetre

Inclut :

- une ADR dediee a la persistance ;
- le positionnement des modules `infrastructure.database`, `application.imports` et `interfaces.cli` ;
- la confirmation que React, FastAPI, worker et Nginx restent hors implementation `v0.2.0` ;
- la strategie d'idempotence et de transactions ;
- le statut des scripts Docker de developpement.

Exclut :

- l'API HTTP ;
- les statistiques ;
- la generation Quarkdown ;
- l'authentification.

### Exigences

- L'ADR doit etre placee dans `docs/architecture/adr/`.
- Le code reste une bibliotheque Python mono-package tant qu'une ADR ulterieure ne cree pas le monorepo applicatif.
- PostgreSQL devient la base cible de `v0.2.0`.
- Les imports doivent etre idempotents par contraintes SQL, pas seulement par verifications Python.
- Toute divergence avec le cahier des charges doit etre documentee.

### Livrables attendus

```text
docs/architecture/adr/ADR-0002-persistance-postgresql-v020.md
```

### Tests

- Verification documentaire par `scripts/check_traceability.py`.
- Absence de reference aux anciens chemins ADR obsoletes.

### Acceptation

- L'ADR explique le perimetre exact de `v0.2.0`.
- L'ADR nomme les decisions reversibles et non reversibles.
- L'ADR decrit comment la v0.2 prepare Docker et l'application complete sans les implementer entierement.

### References

- US-014
