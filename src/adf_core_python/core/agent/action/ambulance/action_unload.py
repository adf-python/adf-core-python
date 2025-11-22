from rcrscore.commands import AKUnload, Command
from rcrscore.entities import EntityID

from adf_core_python.core.agent.action import Action


class ActionUnload(Action):
  def get_command(self, agent_id: EntityID, time: int) -> Command:
    return AKUnload(agent_id, time)

  def __str__(self) -> str:
    return "ActionUnload()"
