# Release report v0.1.0

Statut : `RELEASE_READY`

Mis a jour : 2026-07-25

## Resume

Le lot `v0.1.0` livre le package `atpro` : modeles metier, parseurs CSV,
orchestrateur `ParseFileUseCase`, CLI `atpro file`, fixtures anonymisees,
non-regression et cadrage des CSV reels optionnels.

## Qualite

- `nox -s all` : OK
- Couverture : ≥ 95 % (≈ 97.5 %)
- Twine check : OK
- Traçabilité : OK

## Integrations

Aucune librairie consommatrice obligatoire declaree pour `v0.1.0`.
Composants hors perimetre : PostgreSQL, FastAPI, React, rapports.

## Scan attribution

Messages de commit : presence uniquement de trailers Dependabot / compte projet
(pas d'attribution d'outil de generation interdite).

## Prochaine etape

Merge `version/v0.1.0` → `main`, tag `v0.1.0`, release GitHub.
