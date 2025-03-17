package adf_core_python.component.communication;

import adf_core_python.agent.Agent;
import adf_core_python.agent.communication.MessageManager;

abstract public class CommunicationModule {

    abstract public void receive(Agent agent, MessageManager messageManager);

    abstract public void send(Agent agent, MessageManager messageManager);
}
