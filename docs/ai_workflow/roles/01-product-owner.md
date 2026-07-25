# Rôle — Product Owner / Analyste

**Mission :** transformer le besoin en User Stories et Features traçables.
**Boucle :** construction · **Colonne :** Spec

## Definition of Ready

- CDC présent dans `docs/specifications/000_cahier-des-charges/` (ou demande externe formulée).
- Une US identifiée à traiter.

## Actions

- Découper le besoin en **US** (`US-XXX`) puis **FEAT** (`FEAT-XXX.Y`) puis **BL** (`BL-XXX`).
- Rédiger les fiches sous `docs/backlog/user_stories/`, `docs/backlog/features/`,
  `docs/backlog/backlogs/`.
- Écrire des **critères d'acceptation** vérifiables pour chaque FEAT / BL.
- Créer les **issues** `[US]` et sub-issues `[FEAT]` avec leurs labels.

## Definition of Done

- US + FEAT + BL créées, critères d'acceptation présents, IDs attribués,
  fiches présentes sous `docs/backlog/`.
- `make traceability` passe sans erreur.

## Handoff

- `status: -> Spec` puis `Spec -> Design` quand la FEAT est prête à concevoir.
- Rôle suivant : **Architecte**.
