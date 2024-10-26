from abc import ABC, abstractmethod

from adf_core_python.core.agent.communication.message_manager import MessageManager
from adf_core_python.core.agent.info.agent_info import AgentInfo
from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
from adf_core_python.core.agent.info.world_info import WorldInfo
from adf_core_python.core.component.communication.communication_message import (
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
