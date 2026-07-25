# FEAT-013.1 - Modalite des CSV de reference et tests optionnels

Projet : AT Pro Pilotage  
Version cible : `v0.1.0`  
Type : Feature  
Statut : pret pour implementation

### Intention

Rendre explicite la difference entre fixtures anonymisees et fichiers CSV reels de reference, puis cabler une validation locale optionnelle sur les fichiers reels sans casser la CI.

### Perimetre

Inclut :

- documentation de la modalite retenue pour les CSV reels ;
- convention de chemin local ou variable d'environnement ;
- tests optionnels sur fichiers reels disponibles ;
- message explicite si les fichiers reels sont absents ;
- protection contre l'ajout accidentel de donnees sensibles.

Exclut :

- versionnement de fichiers CSV reels sensibles ;
- import PostgreSQL ;
- stockage applicatif des fichiers ;
- anonymisation industrielle complete des exports reels.

### Exigences

- Les fixtures anonymisees restent les donnees obligatoires de CI.
- Les fichiers reels de reference sont optionnels dans l'environnement de developpement.
- Le chemin par defaut recommande est `samples/reference/` uniquement pour des donnees anonymisees ou explicitement autorisees.
- Pour les fichiers reels sensibles, utiliser une variable d'environnement comme `ATPRO_REFERENCE_CSV_DIR`.
- Les tests sur fichiers reels doivent etre marques ou separables, par exemple `reference`, `slow` ou commande dediee.
- Un test ne doit jamais passer silencieusement parce que le dossier de reference est absent.

### Interfaces attendues

Documentation :

```text
docs/reference-data.md
```

Configuration recommandee :

```text
ATPRO_REFERENCE_CSV_DIR=<chemin local hors depot>
```

Commande de validation recommandee :

```bash
pytest -m reference
```

### Tests obligatoires

- Absence du dossier de reference : skip explicite ou erreur controlee selon commande.
- Presence d'un dossier vide : message explicite.
- Presence de fixtures anonymisees : tests CI OK.
- Presence de fichiers reels : validation parseurs executable localement.

### Acceptation

- La modalite de fourniture des CSV reels est connue avant la fin de `v0.1.0`.
- Les tests de reference ne produisent pas de faux vert.
- Les donnees sensibles ne sont pas ajoutees au depot.

### References

- US-013
