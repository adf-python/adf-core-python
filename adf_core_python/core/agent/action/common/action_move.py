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
        destinationX: Optional[int] = None,
        destinationY: Optional[int] = None,
    ) -> None:
        self.path = path
        self.destinationX = destinationX
        self.destinationY = destinationY

    def get_command(self, agent_id: EntityID, time: int) -> Command:
        path: list[int] = [p.get_value() for p in self.path]
        if self.destinationX is not None and self.destinationY is not None:
            return AKMove(agent_id, time, path, self.destinationX, self.destinationY)
        else:
            return AKMove(agent_id, time, path)

    def __str__(self) -> str:
        return f"ActionMove(path={self.path}, destinationX={self.destinationX}, destinationY={self.destinationY})"
