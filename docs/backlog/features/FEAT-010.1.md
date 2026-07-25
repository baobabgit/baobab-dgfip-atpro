# FEAT-010.1 - Normalisation agents et sites

Projet : AT Pro Pilotage  
Version cible : `v0.1.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Produire une identite brute et normalisee pour les agents et sites.

### Exigences agents

- Conserver le nom brut.
- Normaliser la casse.
- Comparer sans accents.
- Gerer tirets et espaces.
- Reconnaitre autant que possible `NOM Prenom` et `Prenom NOM`.
- Signaler les formes ambigues.

### Exigences sites

- Conserver le site brut.
- Normaliser espaces, casse et accents.
- Ne pas inventer un site absent.

### Sortie attendue

```python
NormalizedIdentity(
    raw_value="Caroline CORBIER",
    normalized_value="caroline corbier",
    first_name_hint="Caroline",
    last_name_hint="CORBIER",
    confidence=...
)
```

### Tests obligatoires

- `NOM Prenom`.
- `Prenom NOM`.
- Nom avec tiret.
- Prenom compose.
- Accent.
- Mauvais encodage partiel.
- Valeur vide.

### Acceptation

- Aucun rapprochement irreversible n'est fait en v0.1.0.



### References

- US-010
