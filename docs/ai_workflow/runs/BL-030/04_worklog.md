# Worklog — BL-030

## Realise

1. Ports `SiteRepository`, `AgentRepository`, `RepositoryWriteOutcome`,
   `RepositoryWriteResult`.
2. Mappers `SiteMapper`, `AgentMapper`.
3. `SqlAlchemySiteRepository` / `SqlAlchemyAgentRepository` avec normalisation
   et resultat created/existing/conflict.
4. Exposition `SqlAlchemyUnitOfWork.sites` / `.agents`.
5. Tests unitaires miroir (creation, reimport, conflit, get, liste inactifs).

## Notes

- Ports separes (1 classe = 1 fichier) plutot que `repositories.py` unique
  demande dans la FEAT (AGENTS.md prime).
