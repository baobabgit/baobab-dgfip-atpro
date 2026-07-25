# Context — BL-019

Dependances satisfaites : readers (BL-012–015), orchestrateur (BL-016), CLI (BL-017),
fixtures anonymisees (BL-018).

Objectif : garantir la robustesse du pipeline (detection → normalisation → readers →
orchestrateur → CLI → erreurs) via une suite de non-regression sur
`tests/fixtures/csv/`, sans baisser le seuil de couverture.
