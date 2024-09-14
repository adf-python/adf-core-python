from typing import TYPE_CHECKING

from rcrs_core.commands.AKExtinguish import AKExtinguish
from rcrs_core.commands.Command import Command
from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.action.action import Action

if TYPE_CHECKING:
    from rcrs_core.commands.Command import Command
    from rcrs_core.worldmodel.entityID import EntityID


class ActionExtinguish(Action):
    def __init__(self, target_id: EntityID, max_power: int) -> None:
        self.target_id = target_id
        self.max_power = max_power

    def get_command(self, agent_id: EntityID, time: int) -> Command:
        # TODO: Implement AKEExtinguish
        return AKExtinguish()

    def __str__(self) -> str:
        return (
            f"ActionExtinguish(target_id={self.target_id}, max_power={self.max_power})"
        )
