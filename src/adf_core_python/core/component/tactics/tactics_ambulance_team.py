from __future__ import annotations

from typing import Optional

from adf_core_python.core.component.tactics import TacticsAgent


class TacticsAmbulanceTeam(TacticsAgent):
  def __init__(self, parent: Optional[TacticsAmbulanceTeam] = None) -> None:
    super().__init__(parent)
