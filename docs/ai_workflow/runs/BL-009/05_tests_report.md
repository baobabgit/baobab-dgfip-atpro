# Tests report — BL-009

## Gates

- black / ruff / mypy / bandit : OK
- pytest : 121+ passed, couverture >= 95 %
- Dependance runtime ajoutee : `tzdata` (fuseau Europe/Paris sous Windows)

## Criteres FEAT-005.3

- Formats date cibles + date francaise + invalide
- Durees secondes / HH:MM:SS / negative / vide
- Pourcentages virgule / vide / invalide
- Texte espaces multiples + accents
- Masquage email / telephone
