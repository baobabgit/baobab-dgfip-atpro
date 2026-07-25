# FEAT-022.1 - Persistance activites journalieres agents

Projet : AT Pro Pilotage  
Version cible : `v0.2.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Enregistrer les activites journalieres agents issues des formats large et long sous une forme commune.

### Perimetre

Inclut :

- repository `AgentDailyActivity` ;
- contrainte agent + date + source ou mesure canonique ;
- stockage des durees et compteurs ;
- lien vers le lot d'import ;
- detection des donnees modifiees.

Exclut :

- occupation horaire complete ;
- reconstruction artificielle des etats agent ;
- statistiques v0.3.0.

### Exigences

- Les formats large et long doivent produire les memes cles metier.
- Une activite identique reimportee ne cree pas de doublon.
- Une activite existante modifiee suit la politique de conflit v0.2.0.
- Les durees doivent etre stockees en secondes ou intervalle selon l'ADR, de facon documentee.

### Livrables attendus

```text
src/atpro/infrastructure/database/repositories/agent_activity_repository.py
tests/infrastructure/database/repositories/test_agent_activity_repository.py
```

### Tests

- Insertion depuis format large normalise.
- Insertion depuis format long normalise.
- Reimport identique.
- Conflit de mesure.

### Acceptation

- Les donnees d'activite v0.1.0 sont disponibles pour les statistiques journalieres v0.3.0.

### References

- US-022
