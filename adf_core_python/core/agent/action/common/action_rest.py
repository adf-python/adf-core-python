from typing import TYPE_CHECKING

from rcrs_core.commands.AKRest import AKRest
from rcrs_core.commands.Command import Command
from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.action.action import Action

if TYPE_CHECKING:
    from rcrs_core.commands.Command import Command
    from rcrs_core.worldmodel.entityID import EntityID


class ActionRest(Action):
    def get_command(self, agent_id: EntityID, time: int) -> Command:
        return AKRest(agent_id, time)

    def __str__(self) -> str:
        return "ActionRest()"
