# FEAT-002.1 - Metadonnees fichier et empreinte SHA-256

Projet : AT Pro Pilotage  
Version cible : `v0.1.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Produire une description stable du fichier inspecte ou parse.

### Champs minimaux

- chemin original ;
- nom de fichier ;
- taille ;
- SHA-256 ;
- encodage detecte ;
- separateur detecte ;
- colonnes brutes ;
- colonnes normalisees ;
- type detecte ;
- version schema ;
- periode detectee ;
- nombre de lignes lues.

### Exigences

- Le SHA-256 doit etre calcule sur le contenu exact du fichier.
- Le calcul doit fonctionner sur gros fichier sans tout charger inutilement en memoire.
- La detection de type ne doit pas dependre uniquement du nom.

### Tests obligatoires

- Deux fichiers identiques donnent le meme SHA-256.
- Un fichier modifie donne un SHA-256 different.
- Fichier vide signale correctement.
- Fichier absent signale correctement.

### Acceptation

- `file inspect` peut afficher ces metadonnees.



### References

- US-002
