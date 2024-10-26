from rcrs_core.agents.agent import Agent

from adf_core_python.core.agent.communication.message_manager import MessageManager
from adf_core_python.core.component.communication.communication_module import (
    CommunicationModule,
)


class StandardCommunicationModule(CommunicationModule):
    def receive(self, agent: Agent, message_manager: MessageManager) -> None:
        raise NotImplementedError

    def send(self, agent: Agent, message_manager: MessageManager) -> None:
        raise NotImplementedError
