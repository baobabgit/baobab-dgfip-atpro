# FEAT-015.1 - PostgreSQL Docker de developpement

Projet : AT Pro Pilotage  
Version cible : `v0.2.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Fournir une base PostgreSQL locale reproductible pour les migrations, les imports et les tests d'integration.

### Perimetre

Inclut :

- un service PostgreSQL dans Docker Compose ;
- un volume persistant de developpement ;
- des variables d'environnement documentees ;
- un healthcheck ;
- une configuration compatible Windows, Linux et CI.

Exclut :

- image applicative backend ;
- image frontend ;
- Nginx ;
- sauvegarde production.

### Exigences

- Utiliser PostgreSQL 17 sauf incompatibilite explicite.
- Le conteneur doit exposer un port configurable.
- Les credentials de developpement ne doivent pas etre reutilises en production.
- Le compose doit permettre de lancer les tests d'integration localement.
- Aucun secret reel ne doit etre commite.

### Livrables attendus

```text
compose.yml ou docker/compose.dev.yml
.env.example
docs/operations/database.md
```

### Tests

- Demarrage du service.
- Verification du healthcheck.
- Connexion avec les variables documentees.

### Acceptation

- Un developpeur peut lancer PostgreSQL sans installer Postgres localement.
- Le service est nomme de maniere stable.
- La documentation indique comment arreter et nettoyer le volume.

### References

- US-015
