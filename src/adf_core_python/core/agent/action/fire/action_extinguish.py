from rcrscore.commands import AKExtinguish, Command
from rcrscore.entities import EntityID

from adf_core_python.core.agent.action import Action


class ActionExtinguish(Action):
  def __init__(self, target_id: EntityID, max_power: int) -> None:
    self.target_id = target_id
    self.max_power = max_power

  def get_command(self, agent_id: EntityID, time: int) -> Command:
    return AKExtinguish(agent_id, time, self.target_id, self.max_power)

  def __str__(self) -> str:
    return f"ActionExtinguish(target_id={self.target_id}, max_power={self.max_power})"
