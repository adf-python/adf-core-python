from abc import ABC, abstractmethod

from rcrs_core.messages.message import Message
from rcrs_core.worldmodel.entityID import EntityID


class Action(ABC):
    @abstractmethod
    def get_command(self, agent_id: EntityID, time: int) -> Message:
        raise NotImplementedError
