# FEAT-026.1 - Annulation controlee d'un import

Projet : AT Pro Pilotage  
Version cible : `v0.2.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Permettre de neutraliser ou supprimer les donnees issues d'un lot d'import de facon controlee.

### Perimetre

Inclut :

- service applicatif de rollback ;
- verification du statut du lot ;
- suppression ou marquage selon l'ADR ;
- mise a jour du statut `rolled_back` ;
- journalisation du resultat.

Exclut :

- restauration automatique d'une version precedente conflictuelle ;
- recalcul des statistiques ;
- annulation via interface Web.

### Exigences

- Le rollback doit etre transactionnel.
- Un lot deja annule ne doit pas etre annule une seconde fois.
- Les donnees partagees avec un autre lot ne doivent pas etre supprimees sans regle explicite.
- Les lignes rejetees et l'historique du lot restent auditables.

### Livrables attendus

```text
src/atpro/application/imports/rollback_import.py
tests/application/imports/test_rollback_import.py
tests/integration/test_import_rollback.py
```

### Tests

- Rollback d'un import complet.
- Rollback d'un import partiellement rejete.
- Tentative sur lot inexistant.
- Tentative sur lot deja annule.

### Acceptation

- Apres rollback, les donnees metier propres au lot ne sont plus prises en compte.

### References

- US-026
