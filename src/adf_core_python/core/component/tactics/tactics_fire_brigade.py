from __future__ import annotations

from typing import Optional

from adf_core_python.core.component.tactics import TacticsAgent


class TacticsFireBrigade(TacticsAgent):
  def __init__(self, parent: Optional[TacticsFireBrigade] = None) -> None:
    super().__init__(parent)
