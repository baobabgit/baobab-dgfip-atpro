# FEAT-002.3 - Registre de schemas et detection du type de fichier

Projet : AT Pro Pilotage  
Version cible : `v0.1.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Identifier automatiquement le type et la variante de schema.

### Types a detecter

- `incoming_calls`;
- `outgoing_calls`;
- `tickets`;
- `agent_activities_wide`;
- `agent_activities_long`;
- `unknown`.

### Exigences

- Utiliser les colonnes presentes.
- Utiliser les noms de mesures si necessaire.
- Gerer l'ordre variable des colonnes.
- Gerer les colonnes supplementaires.
- Signaler les colonnes obligatoires absentes.

### Signatures minimales

Appels :

- identifiant appel ;
- debut appel ;
- fin appel ;
- noms de mesures ;
- valeurs de mesures.

Tickets :

- numero ticket ;
- date creation ou prise en charge ;
- statut ;
- canal ou nature.

Activites large :

- periode ;
- agent/groupe agent ;
- plusieurs colonnes de mesures.

Activites long :

- periode ;
- agent/groupe agent ;
- noms de mesures ;
- valeurs de mesures.

### Tests obligatoires

- Un fichier par type.
- Variante tickets longue.
- Variante tickets reduite.
- Variante activites large.
- Variante activites long.
- Nom de fichier trompeur.

### Acceptation

- La detection retourne type, schema et avertissements.



### References

- US-002
- US-003
