# FEAT-017.2 - Schema relationnel v0.2.0

Projet : AT Pro Pilotage  
Version cible : `v0.2.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Creer les tables PostgreSQL necessaires aux referentiels, imports et donnees metier issues du parseur v0.1.0.

### Perimetre

Inclut :

- tables agents, sites, alias et affectations ;
- tables appels et segments ;
- tables tickets ;
- tables activites journalieres agents ;
- tables lots d'import et lignes rejetees ;
- contraintes d'unicite et index minimaux.

Exclut :

- tables de statistiques ;
- tables de rapports ;
- tables d'authentification.

### Exigences

- Chaque table doit porter des timestamps techniques.
- Les cles metier doivent etre protegees par `UNIQUE`.
- Les relations de provenance doivent permettre un rollback par lot.
- Les donnees personnelles doivent etre limitees au strict necessaire.
- Les colonnes temporelles doivent etre timezone-aware lorsque l'heure est significative.

### Livrables attendus

```text
migrations/versions/*_v020_initial_persistence.py
src/atpro/infrastructure/database/models/
```

### Tests

- Inspection du schema apres migration.
- Verification des contraintes uniques principales.
- Verification des foreign keys.

### Acceptation

- Le schema couvre toutes les sorties canoniques de v0.1.0.
- Les doublons critiques sont impossibles meme en cas d'appel direct SQL.

### References

- US-017
