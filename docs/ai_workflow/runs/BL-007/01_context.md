# Context — BL-007

## Objectif

Service bas niveau d'inspection CSV : empreinte SHA-256 en streaming, détection
encodage / séparateur, lecture et normalisation des en-têtes, sans parser toutes
les lignes métier.

## Dépendances

- BL-006 (diagnostics `parser.results`) : DONE

## Hors périmètre

- Détection de type / version de schéma (BL-008)
- Parseurs métier, CLI `file inspect` (BL ultérieurs)
