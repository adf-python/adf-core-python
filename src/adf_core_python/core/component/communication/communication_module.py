from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from adf_core_python.core.agent import Agent
  from adf_core_python.core.agent.communication import MessageManager


class CommunicationModule(ABC):
  @abstractmethod
  def receive(self, agent: Agent, message_manager: MessageManager) -> None:
    pass

  @abstractmethod
  def send(self, agent: Agent, message_manager: MessageManager) -> None:
    pass
