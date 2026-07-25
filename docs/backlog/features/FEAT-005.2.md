# FEAT-005.2 - Enumerations et value objects

Projet : AT Pro Pilotage  
Version cible : `v0.1.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Centraliser les types partages par les parseurs.

### Enumerations minimales

- `PeriodType`;
- `ScopeType`;
- `ImportFileType`;
- `CallDirection`;
- `ImportSeverity`;
- `ParseStatus`;
- `SchemaVersion`.

### Value objects minimaux

- `ExternalId`;
- `NormalizedText`;
- `RawText`;
- `DurationSeconds`;
- `Percentage`;
- `SourceRowNumber`;
- `FileSha256`;
- `DateRange`;
- `TimezoneName`.

### Exigences

- Les conversions invalides doivent retourner une erreur controlee.
- Les value objects ne doivent pas masquer silencieusement une valeur impossible.
- Les durees sont stockees en secondes.
- Les pourcentages sont stockes en ratio decimal ou pourcentage documente, mais jamais ambigus.

### Tests obligatoires

- Duree en secondes entieres.
- Duree `HH:MM:SS`.
- Pourcentage avec virgule.
- Texte vide.
- Identifiant absent.
- Date range invalide.

### Acceptation

- Les parseurs utilisent ces types au lieu de manipuler uniquement des chaines libres.



### References

- US-005
