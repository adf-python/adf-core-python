from typing import TYPE_CHECKING

from rcrs_core.commands.AKClear import AKClear
from rcrs_core.commands.Command import Command
from rcrs_core.entities.blockade import Blockade
from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.action.action import Action

if TYPE_CHECKING:
    from rcrs_core.commands.Command import Command
    from rcrs_core.worldmodel.entityID import EntityID


class ActionClear(Action):
    def __init__(self, blockade: Blockade) -> None:
        self.blockade = blockade

    def get_command(self, agent_id: EntityID, time: int) -> Command:
        return AKClear(agent_id, time, self.blockade.get_id())

    def __str__(self) -> str:
        return f"ActionClear(blockade={self.blockade})"
