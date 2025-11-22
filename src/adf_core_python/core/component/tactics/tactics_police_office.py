from __future__ import annotations

from typing import Optional

from adf_core_python.core.component.tactics import TacticsCenter


class TacticsPoliceOffice(TacticsCenter):
  def __init__(self, parent: Optional[TacticsPoliceOffice] = None) -> None:
    super().__init__(parent)
