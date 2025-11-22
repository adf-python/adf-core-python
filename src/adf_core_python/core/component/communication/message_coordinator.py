from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from adf_core_python.core.agent.communication import MessageManager
  from adf_core_python.core.agent.info import AgentInfo, ScenarioInfo, WorldInfo
  from adf_core_python.core.component.communication import (
    CommunicationMessage,
  )


class MessageCoordinator(ABC):
  @abstractmethod
  def coordinate(
    self,
    agent_info: AgentInfo,
    world_info: WorldInfo,
    scenario_info: ScenarioInfo,
    message_manager: MessageManager,
    send_message_list: list[CommunicationMessage],
    channel_send_message_list: list[list[CommunicationMessage]],
  ) -> None:
    pass
