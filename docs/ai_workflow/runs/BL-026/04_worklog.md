# Worklog — BL-026

## 2026-07-26

- Port applicatif `UnitOfWork` + implementation `SqlAlchemyUnitOfWork`.
- Erreurs `UnitOfWorkClosedError` / `UnitOfWorkAlreadyCommittedError`.
- Tests SQLite : commit, rollback exception, sans commit, fermeture, double commit.
- Gates : 347 passed, couverture 97.53 %.
