# FEAT-005.1 - Modeles metier canoniques

Projet : AT Pro Pilotage  
Version cible : `v0.1.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Definir les objets metier produits par les parseurs.

### Perimetre

Inclut :

- `Site`;
- `Agent`;
- `AgentAlias`;
- `AgentSiteAssignment`;
- `Call`;
- `CallSegment`;
- `Ticket`;
- `AgentDailyActivity`;
- metadonnees fichier ;
- erreurs et avertissements d'import ;
- resultat de parsing.

Exclut :

- modeles SQLAlchemy ;
- DTO FastAPI ;
- schemas React.

### Exigences

- Les modeles doivent etre independants de l'infrastructure.
- Les modeles doivent etre typables strictement.
- Les modeles doivent etre immutables lorsque cela facilite la securite.
- Chaque modele produit depuis une source doit conserver la provenance minimale.
- Les champs sensibles doivent etre masques ou hashes lorsqu'ils sortent du parsing.

### Interfaces attendues

Noms recommandes :

```python
atpro.domain.sites.Site
atpro.domain.agents.Agent
atpro.domain.calls.Call
atpro.domain.calls.CallSegment
atpro.domain.tickets.Ticket
atpro.domain.activities.AgentDailyActivity
atpro.parser.results.ParseResult
```

### Tests obligatoires

- Instanciation de chaque modele.
- Egalite ou comparaison si utile.
- Serialisation JSON indirecte via fonctions applicatives.
- Validation des champs obligatoires.

### Acceptation

- Aucun modele du domaine n'importe Typer, Polars, SQLAlchemy, FastAPI ou Quarkdown.



### References

- US-005
