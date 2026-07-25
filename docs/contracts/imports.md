# Contrat — Imports publics

> Imports garantis stables pour les consommateurs de ce package.

## Imports garantis (v0.1.0)

```python
import atpro
from atpro import domain, parser, interfaces

from atpro.parser import ParseFileUseCase

from atpro.domain.sites import Site
from atpro.domain.agents import Agent, AgentAlias, AgentSiteAssignment
from atpro.domain.calls import Call, CallSegment
from atpro.domain.tickets import Ticket
from atpro.domain.activities import AgentDailyActivity

from atpro.parser.results import ParseResult, ParsePreview, ParseIssue, FileMetadata
from atpro.interfaces.cli import app, run
```

Le détail des symboles est dans [`public_api.md`](public_api.md) et
[`models.md`](models.md).

## Imports internes (non garantis)

Les sous-modules non exportés dans `__all__` (helpers de readers, détails de
détection, etc.) sont considérés comme internes et peuvent changer sans bump
majeur pendant la phase `0.x`.
