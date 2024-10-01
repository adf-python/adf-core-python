from typing import TYPE_CHECKING, Optional

from rcrs_core.commands.AKMove import AKMove
from rcrs_core.commands.Command import Command
from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.action.action import Action

if TYPE_CHECKING:
    from rcrs_core.commands.Command import Command
    from rcrs_core.worldmodel.entityID import EntityID


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

    def get_command(self, agent_id: EntityID, time: int) -> Command:
        path: list[int] = [p.get_value() for p in self.path]
        if self.destination_x is not None and self.destination_y is not None:
            return AKMove(agent_id, time, path, self.destination_x, self.destination_y)
        else:
            return AKMove(agent_id, time, path)

    def __str__(self) -> str:
        path: str = ", ".join([str(p) for p in self.path])
        return f"ActionMove(path={path}, destination_x={self.destination_x}, destination_y={self.destination_y})"
