package adf_core_python.core.component.communication;

import adf_core_python.core.agent.Agent;
import adf_core_python.core.agent.communication.MessageManager;

abstract public class CommunicationModule {

    abstract public void receive(Agent agent, MessageManager messageManager);

    abstract public void send(Agent agent, MessageManager messageManager);
}
