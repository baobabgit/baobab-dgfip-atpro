# FEAT-012.1 - Fixtures anonymisees et donnees de test

Projet : AT Pro Pilotage  
Version cible : `v0.1.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Disposer de donnees versionnables pour les tests.

### Fichiers recommandes

```text
tests/fixtures/csv/incoming_calls_valid.csv
tests/fixtures/csv/incoming_calls_invalid.csv
tests/fixtures/csv/outgoing_calls_valid.csv
tests/fixtures/csv/tickets_long_valid.csv
tests/fixtures/csv/tickets_short_valid.csv
tests/fixtures/csv/activities_wide_valid.csv
tests/fixtures/csv/activities_long_valid.csv
tests/fixtures/csv/unknown_format.csv
```

### Exigences

- Aucune donnee personnelle reelle.
- Taille reduite.
- Couverture des schemas.
- Cas invalides explicites.

### Tests obligatoires

- Tous les readers ont au moins une fixture valide.
- Au moins une fixture invalide par grande famille.

### Acceptation

- La CI peut tourner sans fichiers reels.



### References

- US-012
