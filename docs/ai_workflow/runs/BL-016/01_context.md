# Context — BL-016

Dependances satisfaites : BL-007 (detection), BL-008 (schemas), BL-012 a BL-015 (readers).

Contrat public : `from atpro.parser import ParseFileUseCase`.

Pas de PostgreSQL. Selection reader selon type/schema detectes.
