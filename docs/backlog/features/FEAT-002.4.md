# FEAT-002.4 - Orchestrateur de parsing

Projet : AT Pro Pilotage  
Version cible : `v0.1.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Fournir un point d'entree unique au parsing.

### Interface recommandee

```python
class ParseFileUseCase:
    def inspect(self, path: Path) -> FileInspection: ...
    def validate(self, path: Path) -> ParseResult: ...
    def preview(self, path: Path, limit: int = 10) -> ParsePreview: ...
    def parse(self, path: Path) -> ParseResult: ...
```

### Exigences

- L'orchestrateur selectionne le reader.
- L'orchestrateur ne connait pas PostgreSQL.
- L'orchestrateur retourne des resultats standardises.
- L'orchestrateur est testable sans CLI.

### Tests obligatoires

- Selection reader appels entrants.
- Selection reader tickets.
- Type inconnu.
- Erreur reader convertie.

### Acceptation

- Le CLI appelle l'orchestrateur, pas les readers directement.



### References

- US-002
- US-004
