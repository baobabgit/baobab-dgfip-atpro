# FEAT-009.1 - Reader activites agents format long

Projet : AT Pro Pilotage  
Version cible : `v0.1.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Parser les fichiers d'activites agents ou chaque ligne est une mesure.

### Exigences

- Detecter format long.
- Grouper par date et agent.
- Mapper les mesures connues.
- Conserver les mesures inconnues.
- Produire une activite par agent et jour.

### Mapping minimal de mesures

- appels decroches ;
- appels recus ;
- duree de mise en garde ;
- nombre d'appels sortants ;
- taux de decroches ;
- taux de mise en garde ;
- temps login ;
- temps non pret ;
- temps pret ;
- temps total dans l'etat rona ;
- temps communication entrants ;
- temps communication sortants ;
- temps post appel ;
- temps telephone.

### Tests obligatoires

- Plusieurs mesures pour meme agent/jour.
- Mesure inconnue.
- Mesure dupliquee identique.
- Mesure dupliquee contradictoire.

### Acceptation

- Le resultat final est un `AgentDailyActivity`, pas une liste brute de mesures.



### References

- US-009
