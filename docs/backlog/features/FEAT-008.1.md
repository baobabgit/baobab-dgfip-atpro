# FEAT-008.1 - Reader activites agents format large

Projet : AT Pro Pilotage  
Version cible : `v0.1.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Parser les fichiers d'activites agents ou chaque mesure est une colonne.

### Exigences

- Detecter format large.
- Produire une activite par agent et jour.
- Convertir compteurs.
- Convertir durees.
- Convertir pourcentages.
- Conserver les mesures supplementaires.

### Tests obligatoires

- Ligne complete.
- Valeurs vides.
- Pourcentage avec virgule.
- Date francaise.
- Agent avec nom compose.

### Acceptation

- Les activites produites sont compatibles avec le format long.



### References

- US-008
