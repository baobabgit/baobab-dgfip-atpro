# Scope v0.1.0

## Objectif

Livrer le socle Python `atpro` capable d'inspecter, valider et previsualiser les CSV de reference en produisant des modeles metier canoniques.

## Inclus

- ADR de structure depot ;
- package `atpro` ;
- modeles metier canoniques ;
- enums et value objects ;
- detection encodage, separateur, type et schema ;
- normalisation textes, dates, durees, pourcentages, agents et sites ;
- readers appels entrants ;
- readers appels sortants ;
- reader tickets ;
- readers activites agents format large et long ;
- orchestrateur de parsing ;
- CLI minimal `file inspect`, `file validate`, `file preview` ;
- fixtures anonymisees ;
- cadrage des CSV reels de reference ;
- contrats publics de librairie ;
- matrice de compatibilite.

## Exclus

- PostgreSQL ;
- migrations ;
- API FastAPI ;
- React ;
- Docker applicatif complet ;
- worker ;
- statistiques ;
- rapports Quarkdown ;
- authentification.

## Backlog

Le backlog actif est `docs/ai_workflow/state/queue.yaml`.

Etat au 25 juillet 2026 : `BL-001` a `BL-006` sont `DONE` (merges sur
`version/v0.1.0`). Le prochain item executable est `BL-007`
(detection fichier), dependances satisfaites.
