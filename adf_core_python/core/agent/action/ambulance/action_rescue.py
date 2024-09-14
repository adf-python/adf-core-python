from typing import TYPE_CHECKING

from rcrs_core.commands.AKRescue import AKRescue
from rcrs_core.commands.Command import Command
from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.action.action import Action

if TYPE_CHECKING:
    from rcrs_core.commands.Command import Command
    from rcrs_core.worldmodel.entityID import EntityID


class ActionRescue(Action):
    def __init__(self, target_id: EntityID) -> None:
        self.target_id = target_id

    def get_command(self, agent_id: EntityID, time: int) -> Command:
        return AKRescue(agent_id, time, self.target_id)

    def __str__(self) -> str:
        return f"ActionRescue(target_id={self.target_id})"
