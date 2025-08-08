from rcrscore.commands import AKRest, Command
from rcrscore.entities import EntityID

from adf_core_python.core.agent.action.action import Action


class ActionRefill(Action):
  def get_command(self, agent_id: EntityID, time: int) -> Command:
    return AKRest(agent_id, time)

  def __str__(self) -> str:
    return "ActionRefill()"
