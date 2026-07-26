# Expected outputs — BL-030

- Ports : SiteRepository, AgentRepository, RepositoryWriteOutcome/Result
- Mappers : SiteMapper, AgentMapper
- Repos : SqlAlchemySiteRepository, SqlAlchemyAgentRepository
- UoW : proprietes `sites` et `agents`
- Tests unitaires miroir (creation, reimport, conflit, get by id, liste inactifs)
- Gates locales vertes
- PR mergee sur `version/v0.2.0`
