from abc import ABC, abstractmethod

from adf_core_python.core.agent.communication.message_manager import MessageManager
from adf_core_python.core.agent.info.agent_info import AgentInfo
from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
from adf_core_python.core.agent.info.world_info import WorldInfo


class ChannelSubscriber(ABC):
    @abstractmethod
    def subscribe(
        self,
        agent_info: AgentInfo,
        world_info: WorldInfo,
        scenario_info: ScenarioInfo,
        message_manager: MessageManager,
    ) -> None:
        """
        Subscribe to the channel.

        Parameters
        ----------
        agent_info : AgentInfo
            The agent info.
        world_info : WorldInfo
            The world info.
        scenario_info : ScenarioInfo
            The scenario info.
        message_manager : MessageManager
            The message manager.
        """
        pass
