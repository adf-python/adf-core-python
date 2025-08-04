from abc import ABC, abstractmethod

from rcrscore.commands import Command
from rcrscore.entities import EntityID


class Action(ABC):
  def __init__(self) -> None:
    pass

  @abstractmethod
  def get_command(self, agent_id: EntityID, time: int) -> Command:
    raise NotImplementedError
