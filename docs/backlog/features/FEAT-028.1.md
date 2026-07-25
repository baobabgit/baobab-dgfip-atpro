# FEAT-028.1 - Tests d'integration PostgreSQL

Projet : AT Pro Pilotage  
Version cible : `v0.2.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Verifier les migrations, repositories, imports idempotents et rollbacks contre un vrai PostgreSQL.

### Perimetre

Inclut :

- marqueur pytest `integration` ou `postgresql` ;
- fixtures de base temporaire ;
- execution des migrations avant tests ;
- nettoyage fiable ;
- scenarios de non-regression.

Exclut :

- tests frontend ;
- tests de charge lourds ;
- CI complete de deploiement.

### Exigences

- Les tests ne doivent pas dependre d'une base locale non documentee.
- Les warnings pytest doivent etre declares dans `pyproject.toml`.
- Les tests d'integration peuvent etre separes des tests unitaires mais doivent etre documentes.
- La couverture globale imposee par le depot reste la cible tant qu'aucune ADR ne la module.

### Livrables attendus

```text
tests/integration/
tests/conftest.py
pyproject.toml
docs/operations/testing.md
```

### Tests

- Migration sur base vide.
- Idempotence d'import.
- Contraintes uniques.
- Rollback.

### Acceptation

- Une commande documentee permet de lancer les tests PostgreSQL.
- Aucun warning pytest non declare n'est introduit.

### References

- US-028
