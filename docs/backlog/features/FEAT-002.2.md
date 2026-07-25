# FEAT-002.2 - Detection encodage, separateur et en-tetes

Projet : AT Pro Pilotage  
Version cible : `v0.1.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Lire des CSV heterogenes sans configuration manuelle.

### Encodages a supporter

- UTF-8 ;
- UTF-8 avec BOM ;
- Windows-1252 ;
- detection degradee avec avertissement.

### Separateurs a supporter

- `;` obligatoire ;
- `,` optionnel ;
- tabulation optionnelle.

### Exigences

- La detection doit inspecter un echantillon suffisant.
- Les en-tetes doivent etre normalises pour comparaison.
- Les accents mal encodes doivent etre geres autant que possible.
- Le resultat doit indiquer le niveau de confiance si disponible.

### Tests obligatoires

- CSV avec `;`.
- CSV avec guillemets.
- En-tetes avec accents.
- En-tetes mal encodes.
- Fichier sans en-tete.

### Acceptation

- Les fichiers de reference connus sont lisibles.



### References

- US-002
- US-003
