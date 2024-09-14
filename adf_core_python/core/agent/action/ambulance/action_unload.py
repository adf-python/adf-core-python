from typing import TYPE_CHECKING

from rcrs_core.commands.AKUnload import AKUnload
from rcrs_core.commands.Command import Command
from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.action.action import Action

if TYPE_CHECKING:
    from rcrs_core.commands.Command import Command
    from rcrs_core.worldmodel.entityID import EntityID


class ActionUnload(Action):
    def get_command(self, agent_id: EntityID, time: int) -> Command:
        return AKUnload(agent_id, time)

    def __str__(self) -> str:
        return "ActionUnload()"
