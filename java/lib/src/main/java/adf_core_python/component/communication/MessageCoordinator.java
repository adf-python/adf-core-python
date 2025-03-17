package adf_core_python.component.communication;

import adf.core.agent.info.ScenarioInfo;
import adf.core.agent.info.WorldInfo;
import adf.core.component.communication.CommunicationMessage;
import adf_core_python.agent.communication.MessageManager;
import adf_core_python.agent.info.AgentInfo;

import java.util.ArrayList;
import java.util.List;

abstract public class MessageCoordinator {

    abstract public void coordinate(AgentInfo agentInfo, WorldInfo worldInfo,
                                    ScenarioInfo scenarioInfo, MessageManager messageManager,
                                    ArrayList<CommunicationMessage> sendMessageList,
                                    List<List<CommunicationMessage>> channelSendMessageList);
}
