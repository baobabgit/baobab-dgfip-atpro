# Changelog

Toutes les modifications notables de ce projet sont documentées ici.

Le format suit [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [0.1.0] - 2026-07-25

Première livraison du package Python ``atpro`` (pilotage AT Pro / DGFiP) :
modèles métier, parseurs CSV, orchestrateur et CLI ``atpro file``.

### Ajouté

- Package ``atpro`` : domaine (``Site``, ``Agent``, ``Call``, ``CallSegment``,
  ``Ticket``, ``AgentDailyActivity``, enums, value objects).
- Parseurs CSV : détection fichier, schémas, normalizers, readers (appels
  entrants/sortants, tickets, activités wide/long), consolidation d'appels.
- Orchestrateur ``ParseFileUseCase`` (``inspect`` / ``validate`` / ``preview`` /
  ``parse``).
- CLI Typer ``atpro file`` (codes de sortie 0–4, options ``--json`` / ``--limit``).
- Fixtures CSV anonymisées ``tests/fixtures/csv/`` et suite de non-régression.
- Validation optionnelle des CSV réels via ``ATPRO_REFERENCE_CSV_DIR``
  (marqueur pytest ``reference``, ``make reference-test``).
- Contrats publics, guides développeur, ADR-0001, documentation de référence.
- Dépendances runtime : ``pydantic-settings``, ``tzdata``, ``typer``.

### Limites (hors périmètre v0.1.0)

- Pas de PostgreSQL, API HTTP, frontend React, statistiques ni rapports.

## [Unreleased]

### Notes

- Les entrées historiques du template d'outillage (avant le lot produit AT Pro)
  restent disponibles dans l'historique Git.
