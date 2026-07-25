# Fixtures CSV anonymisées

Données synthétiques françaises pour les tests et la CI.
**Aucune donnée personnelle réelle** — personnages fictifs uniquement
(Alice DUPONT, Bob MARTIN, numéros `0611111111` / `0142000000`, sites Paris / Lyon / Lille).

Séparation `;`, encodage UTF-8. Schémas alignés sur `SchemaRegistry` (FEAT-012.1).

## Fichiers valides

| Fichier | Schéma | Usage |
|---|---|---|
| `incoming_calls_valid.csv` | `incoming_calls_v1` | Appels entrants multi-mesures / multi-appels |
| `outgoing_calls_valid.csv` | `outgoing_calls_v1` | Appels sortants (numéro appelant vide) |
| `tickets_long_valid.csv` | `tickets_long` | Tickets complets (clos + ouvert) |
| `tickets_short_valid.csv` | `tickets_reduced` | Tickets schéma réduit |
| `activities_wide_valid.csv` | `activities_wide` | Activités agents format large |
| `activities_long_valid.csv` | `activities_long` | Activités agents format long |

## Fichiers invalides / edge

| Fichier | Famille | Erreur attendue |
|---|---|---|
| `incoming_calls_invalid.csv` | Appels entrants | `CALL_END_BEFORE_START` |
| `outgoing_calls_invalid.csv` | Appels sortants | `CALL_END_BEFORE_START` |
| `tickets_invalid.csv` | Tickets | `TICKET_RESOLVED_BEFORE_CREATED` |
| `activities_invalid.csv` | Activités | `ACTIVITY_MEASURE_CONFLICT` |
| `unknown_format.csv` | Inconnu | `FILE_TYPE_UNKNOWN` via `ParseFileUseCase` |

## Consommation

Chemin typique depuis les tests :

```python
from pathlib import Path

FIXTURES_CSV = Path(__file__).resolve().parents[3] / "fixtures" / "csv"
```

Les readers (`IncomingCallsReader`, …) et `ParseFileUseCase.parse` doivent charger
les fixtures valides sans erreur bloquante.
