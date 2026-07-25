# FEAT-028.2 - Documentation, contrats et release v0.2.0

Projet : AT Pro Pilotage  
Version cible : `v0.2.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Mettre a jour les contrats publics, la documentation d'exploitation et le suivi workflow pour que la v0.2.0 soit exploitable par une IA de developpement.

### Perimetre

Inclut :

- contrat de persistance ;
- documentation des commandes ;
- documentation Docker/PostgreSQL ;
- dossier `docs/ai_workflow/versions/v0.2.0/` ;
- matrice de compatibilite ;
- release report preparatoire.

Exclut :

- documentation React ;
- documentation API FastAPI ;
- runbook production complet.

### Exigences

- Aucun document ne doit referencer le template `example_package`.
- Les chemins doivent rester compatibles avec le workflow AGENTS.
- Les criteres d'acceptation v0.2.0 doivent etre verifies ou marques explicitement non faits.
- La trace US -> FEAT -> BL doit rester valide.

### Livrables attendus

```text
docs/contracts/persistence_contract.md
docs/operations/database.md
docs/operations/imports.md
docs/ai_workflow/versions/v0.2.0/
```

### Tests

- `python scripts/check_traceability.py`.
- Relecture des contrats publics.

### Acceptation

- La v0.2.0 dispose d'un dossier de version complet.
- Les futurs developpeurs savent lancer la base, migrer, importer et tester.

### References

- US-028
