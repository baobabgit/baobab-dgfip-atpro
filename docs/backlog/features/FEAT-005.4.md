# FEAT-005.4 - Reader appels entrants

Projet : AT Pro Pilotage  
Version cible : `v0.1.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Parser et consolider les fichiers d'appels entrants.

### Exigences

- Lire les lignes de mesures.
- Identifier `Duree de communication`.
- Identifier `Duree de mise en garde`.
- Regrouper les mesures par appel et segment.
- Produire `Call(direction=incoming)`.
- Produire `CallSegment`.
- Conserver les lignes sources.
- Detecter multi-segments.
- Masquer ou hasher les numeros.

### Erreurs et avertissements

- identifiant appel absent : erreur ;
- debut ou fin invalide : erreur ;
- fin avant debut : erreur ;
- mesure inconnue : avertissement ;
- agent vide : avertissement severe ;
- duree contradictoire : erreur ou avertissement severe selon cas.

### Tests obligatoires

- Appel simple avec deux lignes de mesures.
- Appel avec duree zero.
- Appel multi-segments.
- Mesure inconnue.
- Date au format historique.

### Acceptation

- La consolidation ne perd pas de mesure.



### References

- US-005
