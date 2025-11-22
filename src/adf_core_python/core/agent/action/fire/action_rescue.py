from rcrscore.commands import AKRescue, Command
from rcrscore.entities import EntityID

from adf_core_python.core.agent.action import Action


class ActionRescue(Action):
  def __init__(self, target_id: EntityID) -> None:
    self.target_id = target_id

  def get_command(self, agent_id: EntityID, time: int) -> Command:
    return AKRescue(agent_id, time, self.target_id)

  def __str__(self) -> str:
    return f"ActionRescue(target_id={self.target_id})"
