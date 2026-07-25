# FEAT-025.1 - Quarantaine des lignes rejetees

Projet : AT Pro Pilotage  
Version cible : `v0.2.0`  
Type : Feature  
Statut : pret pour implementation


### Intention

Conserver les lignes non importables avec un diagnostic utile, sans exposer inutilement de donnees personnelles.

### Perimetre

Inclut :

- modele de ligne rejetee ;
- masquage des champs sensibles ;
- motif, severite, numero de ligne source ;
- rattachement au lot d'import ;
- consultation CLI.

Exclut :

- correction interactive ;
- reimport automatique depuis quarantaine ;
- stockage brut illimite.

### Exigences

- Les numeros de telephone et emails doivent etre masques ou haches.
- Le contenu conserve doit etre suffisant pour comprendre l'erreur.
- Les erreurs de parsing v0.1.0 doivent etre preservables.
- Les rejets ne doivent pas empecher l'import des lignes valides sauf erreur bloquante.

### Livrables attendus

```text
src/atpro/application/imports/rejected_rows.py
src/atpro/infrastructure/privacy/masking.py
tests/application/imports/test_rejected_rows.py
```

### Tests

- Masquage telephone.
- Masquage email.
- Conservation numero de ligne.
- Consultation des rejets d'un lot.

### Acceptation

- Le CLI peut afficher les erreurs d'import sans fuite evidente de donnees sensibles.

### References

- US-019
- US-025
