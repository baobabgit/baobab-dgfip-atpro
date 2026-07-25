"""Ports applicatifs (interfaces sans dependance infrastructure).

:spec: FEAT-016.2
"""

from __future__ import annotations

from atpro.application.ports.unit_of_work import UnitOfWork

__all__: list[str] = ["UnitOfWork"]
