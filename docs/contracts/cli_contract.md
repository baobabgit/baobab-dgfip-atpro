# Contrat CLI v0.1.0

Commande racine : `atpro`

## Commandes publiques

```bash
atpro file inspect <path>
atpro file validate <path>
atpro file preview <path>
```

## Options minimales

- `--json`
- `--limit` pour `preview`

## Codes de sortie recommandes

| Code | Signification |
|---:|---|
| 0 | Succes |
| 1 | Fichier invalide |
| 2 | Fichier introuvable ou illisible |
| 3 | Format inconnu |
| 4 | Erreur technique |

## Contraintes

- Le CLI appelle les cas d'usage Python.
- Le CLI ne contient pas de logique metier.
- Le CLI ne persiste aucune donnee.
- Le CLI ne doit pas afficher de donnees sensibles brutes dans les sorties longues.
