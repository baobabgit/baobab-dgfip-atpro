# FEAT-007.1 - Reader tickets

Projet : AT Pro Pilotage  
Version cible : `v0.1.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Parser les fichiers tickets historiques et reduits.

### Exigences

- Supporter schema long.
- Supporter schema reduit.
- Produire `Ticket`.
- Gerer dates de creation, prise en charge, resolution, cloture.
- Gerer tickets ouverts.
- Normaliser canaux, natures, types, statuts.
- Construire agents bruts et normalises.
- Construire sites bruts et normalises.
- Masquer contacts sensibles.

### Erreurs et avertissements

- numero ticket absent : erreur ;
- date creation absente : avertissement severe ou erreur selon schema ;
- resolution avant creation : erreur ;
- cloture avant creation : erreur ;
- site absent : avertissement ;
- agent absent : avertissement.

### Tests obligatoires

- Ticket clos complet.
- Ticket ouvert.
- Schema long.
- Schema reduit.
- Encodage degrade.
- Date incoherente.

### Acceptation

- Les tickets sans resolution ne sont pas rejetes automatiquement.



### References

- US-007
