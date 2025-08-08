from rcrscore.commands import AKClear, Command
from rcrscore.entities import Blockade, EntityID

from adf_core_python.core.agent.action.action import Action


class ActionClear(Action):
  def __init__(self, blockade: Blockade) -> None:
    self.blockade = blockade

  def get_command(self, agent_id: EntityID, time: int) -> Command:
    return AKClear(agent_id, time, self.blockade.get_entity_id())

  def __str__(self) -> str:
    return f"ActionClear(blockade={self.blockade})"
