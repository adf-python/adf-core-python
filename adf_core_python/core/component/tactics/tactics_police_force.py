from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from adf_core_python.core.component.tactics.tactics_agent import TacticsAgent


class TacticsPoliceForce(TacticsAgent):
    def __init__(self, parent: Optional[TacticsPoliceForce] = None) -> None:
        super().__init__(parent)