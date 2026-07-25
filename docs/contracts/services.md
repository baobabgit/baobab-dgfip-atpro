# Contrat — Services publics

> Services (classes avec logique métier) exposés pour `v0.1.0`.

## Services / cas d'usage

| Classe | Module | Rôle |
|---|---|---|
| `ParseFileUseCase` | `atpro.parser` | Orchestrateur inspect / parse / preview |
| `FileCliService` | `atpro.interfaces.cli.file_cli_service` | Adaptation CLI → use case |
| `SchemaRegistry` | `atpro.parser.schemas` | Catalogue des schémas CSV |
| `SchemaDetector` | `atpro.parser.schemas` | Détection de schéma |
| `FileInspector` | `atpro.parser.detection` | Inspection bas niveau |

Readers et normalizers : voir [`parser_contract.md`](parser_contract.md).  
CLI : voir [`cli_contract.md`](cli_contract.md).  
API publique : voir [`public_api.md`](public_api.md).

## Hors services v0.1.0

Services HTTP, accès SQL / persistence, calculateurs statistiques, générateurs de
rapports.
