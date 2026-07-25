# FEAT-002.5 - CLI minimal `file`

Projet : AT Pro Pilotage  
Version cible : `v0.1.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Permettre l'exploitation du parsing depuis le terminal.

### Commandes

```bash
atpro file inspect <path>
atpro file validate <path>
atpro file preview <path>
```

### Options minimales

- `--json`;
- `--limit` pour preview ;
- `--verbose` optionnel.

### Exigences

- Codes de sortie coherents.
- Sortie humaine lisible.
- Sortie JSON stable.
- Aucun acces base.
- Aucun calcul statistique.

### Codes de sortie recommandes

| Code | Signification |
|---:|---|
| 0 | Succes |
| 1 | Fichier invalide |
| 2 | Fichier introuvable ou illisible |
| 3 | Format inconnu |
| 4 | Erreur technique |

### Tests obligatoires

- Chaque commande en succes.
- Fichier absent.
- Format inconnu.
- Sortie JSON valide.

### Acceptation

- Les commandes permettent de valider les fichiers de reference ou fixtures.



### References

- US-002
- US-004
