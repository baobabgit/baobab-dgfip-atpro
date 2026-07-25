# FEAT-017.1 - Initialisation Alembic

Projet : AT Pro Pilotage  
Version cible : `v0.2.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Introduire Alembic comme mecanisme officiel de migration PostgreSQL du projet.

### Perimetre

Inclut :

- configuration Alembic ;
- environnement de migration connecte a la configuration projet ;
- commande documentee pour appliquer les migrations ;
- integration avec le workflow de tests.

Exclut :

- migration production automatisee ;
- downgrade destructif complexe ;
- donnees de reference initiales si elles ne sont pas strictement necessaires.

### Exigences

- Les migrations doivent cibler PostgreSQL.
- Les noms de revisions doivent etre lisibles.
- Le dossier de migrations doit etre stable et documente.
- L'execution ne doit pas dependre d'un chemin absolu local.

### Livrables attendus

```text
migrations/
alembic.ini
docs/operations/database.md
```

### Tests

- `upgrade head` sur base vide.
- `downgrade base` si supporte par la migration.
- Verification que les metadonnees SQLAlchemy sont importables.

### Acceptation

- Une base PostgreSQL vide peut recevoir le schema v0.2.0 par Alembic.
- Les consignes d'utilisation sont presentes dans la documentation.

### References

- US-017
