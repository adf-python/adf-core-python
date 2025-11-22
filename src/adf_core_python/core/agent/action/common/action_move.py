from typing import Optional

from rcrscore.commands import AKMove, Command
from rcrscore.entities import EntityID

from adf_core_python.core.agent.action import Action


class ActionMove(Action):
  def __init__(
    self,
    path: list[EntityID],
    destination_x: Optional[int] = None,
    destination_y: Optional[int] = None,
  ) -> None:
    self.path = path
    self.destination_x = destination_x
    self.destination_y = destination_y

  def is_destination_defined(self) -> bool:
    return self.destination_x is not None and self.destination_y is not None

  def get_destination_x(self) -> Optional[int]:
    return self.destination_x

  def get_destination_y(self) -> Optional[int]:
    return self.destination_y

  def get_command(self, agent_id: EntityID, time: int) -> Command:
    if self.destination_x is not None and self.destination_y is not None:
      return AKMove(agent_id, time, self.path, self.destination_x, self.destination_y)
    else:
      return AKMove(agent_id, time, self.path)

  def __str__(self) -> str:
    path: str = ", ".join([str(p) for p in self.path])
    return f"ActionMove(path={path}, destination_x={self.destination_x}, destination_y={self.destination_y})"
