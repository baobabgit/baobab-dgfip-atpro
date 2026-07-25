# FEAT-015.2 - Configuration base de donnees

Projet : AT Pro Pilotage  
Version cible : `v0.2.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Centraliser la configuration de connexion PostgreSQL pour le CLI, les migrations, les repositories et les tests.

### Perimetre

Inclut :

- lecture des variables d'environnement ;
- construction de l'URL SQLAlchemy ;
- valeurs par defaut de developpement ;
- configuration separee pour les tests ;
- messages d'erreur lisibles en cas de configuration incomplete.

Exclut :

- gestion de secrets production ;
- rotation de mots de passe ;
- configuration multi-tenant.

### Exigences

- La configuration doit etre testable sans ouvrir de connexion reseau.
- Les valeurs sensibles ne doivent pas etre affichees en clair dans les logs.
- Le module de configuration ne doit pas dependre du CLI.
- Les tests doivent pouvoir injecter une URL PostgreSQL temporaire.

### Livrables attendus

```text
src/atpro/infrastructure/config/
tests/infrastructure/config/
.env.example
```

### Tests

- Cas complet avec URL explicite.
- Cas compose depuis host, port, base, user et password.
- Cas erreur avec variable obligatoire absente.
- Masquage du mot de passe dans les representations.

### Acceptation

- Une seule source de verite construit la configuration PostgreSQL.
- Les migrations, le CLI et les repositories peuvent consommer la meme configuration.

### References

- US-015
