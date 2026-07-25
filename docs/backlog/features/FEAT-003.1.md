# FEAT-003.1 - Validation, erreurs et avertissements

Projet : AT Pro Pilotage  
Version cible : `v0.1.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Fournir un systeme uniforme de diagnostic.

### Types attendus

- `ImportError`;
- `ImportWarning`;
- `ValidationIssue`;
- `ParseSummary`.

### Champs minimaux d'une issue

- code ;
- message ;
- severity ;
- row_number ;
- column ;
- raw_value masquee si sensible ;
- hint technique optionnel.

### Niveaux de severite

- `info`;
- `warning`;
- `error`;
- `fatal`.

### Exigences

- Les erreurs doivent etre stables pour les tests.
- Les messages doivent etre comprehensibles.
- Les exceptions techniques doivent etre capturees et converties.

### Tests obligatoires

- Erreur avec ligne.
- Erreur sans ligne.
- Avertissement non bloquant.
- Erreur fatale.
- Serialisation JSON.

### Acceptation

- Tous les readers utilisent ce modele.



### References

- US-003
- US-011
