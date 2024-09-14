from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rcrs_core.commands.Command import Command
    from rcrs_core.worldmodel.entityID import EntityID


class Action(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_command(self, agent_id: EntityID, time: int) -> Command:
        raise NotImplementedError
