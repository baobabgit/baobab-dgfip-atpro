"""Package applicatif AT Pro Pilotage.

:spec: FEAT-001.1
"""

from __future__ import annotations

from atpro import domain, interfaces, parser

__all__: list[str] = ["__version__", "domain", "interfaces", "parser"]

__version__: str = "0.1.0"
