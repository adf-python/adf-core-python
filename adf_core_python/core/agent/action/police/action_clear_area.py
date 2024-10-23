from typing import TYPE_CHECKING

from rcrs_core.commands.AKClearArea import AKClearArea
from rcrs_core.commands.Command import Command
from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.action.action import Action

if TYPE_CHECKING:
    from rcrs_core.commands.Command import Command
    from rcrs_core.worldmodel.entityID import EntityID


class ActionClearArea(Action):
    def __init__(self, position_x: int, position_y: int) -> None:
        self.position_x = position_x
        self.position_y = position_y

    def get_position_x(self) -> int:
        return self.position_x

    def get_position_y(self) -> int:
        return self.position_y

    def get_command(self, agent_id: EntityID, time: int) -> Command:
        return AKClearArea(agent_id, time, self.position_x, self.position_y)

    def __str__(self) -> str:
        return f"ActionClearArea(position_x={self.position_x}, position_y={self.position_y})"
