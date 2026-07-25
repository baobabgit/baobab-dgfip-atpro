# Release report v0.1.0

Statut : `IN_DEVELOPMENT`

Mis a jour : 2026-07-25

## Resume

Le lot `v0.1.0` est en cours. Les backlogs `BL-001` a `BL-006` sont merges sur
`version/v0.1.0`. Le prochain item executable est `BL-007`.

## Etat des livrables

| Livrable | Etat |
|---|---|
| ADR-0001 | DONE (PR #9) |
| Backlog v0.1.0 | DONE (fiches US/FEAT/BL) |
| Queue active | DONE (`BL-001`..`BL-006` DONE, `BL-007` READY) |
| Graphe de dependances | DONE |
| Contrats publics | Cadres (alignement code progressif) |
| CSV de reference | Cadres (`docs/reference-data.md`) ; fixtures BL-018 |
| Package `atpro` | En cours (`src/atpro` present) |
| Domaine (enums, VOs, modeles) | DONE (BL-003..BL-005) |
| Diagnostics parsing (`ParseResult`, etc.) | DONE (BL-006) |
| Detection fichier / readers / CLI | A developper (BL-007+) |
| Tests | En place pour le code livre ; couverture >= 95 % |
| Runs BL-001..BL-006 | MERGED (piste d'audit synchronisee, PR #15) |

## PRs mergees sur `version/v0.1.0`

| BL | PR | Merge |
|---|---|---|
| BL-001 | [#9](https://github.com/baobabgit/baobab-dgfip-atpro/pull/9) | 2026-07-25T10:48:09Z |
| BL-002 | [#10](https://github.com/baobabgit/baobab-dgfip-atpro/pull/10) | 2026-07-25T10:51:55Z |
| BL-003 | [#11](https://github.com/baobabgit/baobab-dgfip-atpro/pull/11) | 2026-07-25T10:54:40Z |
| BL-004 | [#12](https://github.com/baobabgit/baobab-dgfip-atpro/pull/12) | 2026-07-25T10:57:33Z |
| BL-005 | [#13](https://github.com/baobabgit/baobab-dgfip-atpro/pull/13) | 2026-07-25T11:52:03Z |
| BL-006 | [#14](https://github.com/baobabgit/baobab-dgfip-atpro/pull/14) | 2026-07-25T11:54:37Z |
| Bookkeeping runs | [#15](https://github.com/baobabgit/baobab-dgfip-atpro/pull/15) | 2026-07-25T12:07:41Z |

## Conditions de passage a RELEASE_READY

- Tous les items `BL-001` a `BL-021` termines.
- Validation traceability OK.
- Validation qualite OK (`make all` / equivalent `uv`).
- Contrats publics alignes avec le code.
- Documentation reference data exploitable.
- Rapport de release finalise.
