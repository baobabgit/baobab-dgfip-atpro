# FEAT-021.1 - Persistance tickets

Projet : AT Pro Pilotage  
Version cible : `v0.2.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Enregistrer les tickets normalises avec leurs dates, statuts, canaux, agents et sites de rattachement.

### Perimetre

Inclut :

- repository `Ticket` ;
- contrainte `source_system + ticket_number` ;
- liens vers agents et sites lorsque resolus ;
- conservation des champs utiles aux statistiques futures ;
- lien vers le lot d'import ;
- detection de modification sur ticket deja connu.

Exclut :

- calcul des delais ;
- backlog historique exact ;
- rapprochement telephonie-ticket.

### Exigences

- Les dates incoherentes doivent etre refusees ou mises en quarantaine selon la validation v0.1.0.
- Les champs optionnels doivent rester optionnels en base si les exports ne les fournissent pas.
- Les donnees personnelles non utiles ne doivent pas etre stockees.
- Les variantes de schema ticket doivent converger vers une table canonique.

### Livrables attendus

```text
src/atpro/infrastructure/database/repositories/ticket_repository.py
tests/infrastructure/database/repositories/test_ticket_repository.py
```

### Tests

- Insertion ticket complet.
- Insertion ticket avec champs optionnels absents.
- Reimport identique ignore.
- Conflit de contenu detecte.

### Acceptation

- Les tickets v0.1.0 issus des schemas connus peuvent etre persistés sans perte fonctionnelle.

### References

- US-021
