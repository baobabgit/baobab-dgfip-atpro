# Context — BL-021

- Dépendances : BL-018 (fixtures), BL-019 (non-régression) livrées.
- `docs/reference-data.md` existait avec des points ouverts → décision v0.1.0
  à trancher et à câbler.
- Helper : `ReferenceDataLocator` sous `atpro.testing` (hors contrat public).
- CI = fixtures `tests/fixtures/csv/` ; local optionnel = env + marqueur
  `reference`.
