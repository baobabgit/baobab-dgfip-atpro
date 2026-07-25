# FEAT-005.3 - Normalisation texte, dates, durees et pourcentages

Projet : AT Pro Pilotage  
Version cible : `v0.1.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Convertir les valeurs brutes en valeurs metier fiables.

### Dates a supporter

- `dd/MM/yyyy HH:mm:ss`;
- `dd-MM-yy HH:mm:ss`;
- `yyyy/MM/dd`;
- date francaise comme `15 juin 2026`.

### Durees a supporter

- secondes entieres ;
- `HH:MM:SS`;
- valeur vide interpretee selon contexte.

### Pourcentages a supporter

- `100,00%`;
- `0,00%`;
- valeur vide ;
- valeur numerique sans `%` si documentee.

### Exigences

- Fuseau par defaut : `Europe/Paris`.
- Les dates parsees doivent etre timezone-aware ou accompagnees d'un fuseau d'interpretation.
- Les conversions invalides doivent produire une erreur localisee.
- Les conversions ne doivent pas lever d'exception brute jusqu'au CLI.

### Tests obligatoires

- Tous les formats ci-dessus.
- Date invalide.
- Duree negative.
- Pourcentage invalide.
- Texte avec espaces multiples.

### Acceptation

- Les readers n'implementent pas chacun leur propre parseur de date ou duree.



### References

- US-005
