from __future__ import annotations

from typing import Optional

from adf_core_python.core.component.tactics.tactics_center import TacticsCenter


class TacticsAmbulanceCenter(TacticsCenter):
  def __init__(self, parent: Optional[TacticsAmbulanceCenter] = None) -> None:
    super().__init__(parent)
