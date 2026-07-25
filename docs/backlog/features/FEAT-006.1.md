# FEAT-006.1 - Reader appels sortants

Projet : AT Pro Pilotage  
Version cible : `v0.1.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Parser les fichiers d'appels sortants et contre-appels.

### Exigences

- Produire `Call(direction=outgoing)`.
- Gerer numero appelant vide.
- Gerer absence de flux/service.
- Consolider les mesures comme pour appels entrants.
- Detecter le fichier meme si le nom contient une faute.

### Tests obligatoires

- Fichier avec numero appelant vide.
- Fichier au nom trompeur.
- Appel avec communication et mise en garde.
- Colonnes optionnelles absentes.

### Acceptation

- Les appels sortants ne sont pas rejetes pour absence de flux/service.



### References

- US-006
