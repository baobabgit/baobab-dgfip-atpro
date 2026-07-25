# Context — BL-017

- Dependance : BL-016 (`ParseFileUseCase`) livree.
- Contrat : `docs/contracts/cli_contract.md`, `docs/contracts/public_api.md` (`atpro.interfaces.cli`).
- Pas d'acces DB, pas de logique metier dans le CLI.
- Codes de sortie FEAT-002.5 : 0 succes, 1 invalide, 2 absent/illisible, 3 format inconnu, 4 technique.
