package adf_core_python.core.gateway;

import adf.core.agent.develop.DevelopData;
import adf.core.agent.info.ScenarioInfo;
import adf.core.launcher.ConfigKey;
import adf_core_python.core.agent.Agent;
import adf_core_python.core.agent.config.ModuleConfig;
import adf_core_python.core.gateway.message.*;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import rescuecore2.config.Config;
import rescuecore2.messages.Command;
import rescuecore2.messages.Message;
import rescuecore2.messages.protobuf.RCRSProto;
import rescuecore2.messages.protobuf.RCRSProto.MessageProto;
import rescuecore2.misc.EncodingTools;
import rescuecore2.worldmodel.ChangeSet;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import java.util.Collection;
import java.util.HashMap;

public class Coordinator extends Thread {
    private final InputStream inputStream;
    private final OutputStream outputStream;
    private final HashMap<Integer, ChangeSet> changeSetTemp = new HashMap<>();
    private final HashMap<Integer, Collection<Command>> heardTemp = new HashMap<>();
    private boolean running = true;
    private Agent agent;

    public Coordinator(Socket socket) {
        try {
            socket.setSoTimeout(1000);
            socket.setReuseAddress(true);
            inputStream = socket.getInputStream();
            outputStream = socket.getOutputStream();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        Logger logger = LogManager.getLogger(this.getClass());
        logger.info("Connected from {} on {}", socket.getRemoteSocketAddress(), socket.getLocalSocketAddress());
    }

    @Override
    public void run() {
        while (running) {
            RCRSProto.MessageProto messageProto = receiveMessage();
            if (messageProto == null) continue;
            try {
                Message message = ModuleControlMessageFactory.makeMessage(messageProto.getUrn(), messageProto);
                handleMessage(message);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
    }

    private void handleMessage(Message message) {
        if (message instanceof AMAgent amAgent) {
            ScenarioInfo.Mode mode = ScenarioInfo.Mode.NON_PRECOMPUTE;
            switch (amAgent.getMode()) {
                case 1:
                    mode = ScenarioInfo.Mode.PRECOMPUTED;
                    break;
                case 2:
                    mode = ScenarioInfo.Mode.PRECOMPUTATION_PHASE;
                    break;
            }
            Config config = amAgent.getConfig();
            agent = new Agent(amAgent.getAgentID(), amAgent.getEntities(), new ScenarioInfo(config, mode), new DevelopData(
                    config.getBooleanValue(ConfigKey.KEY_DEVELOP_FLAG, false),
                    config.getValue(ConfigKey.KEY_DEVELOP_DATA_FILE_NAME,
                            DevelopData.DEFAULT_FILE_NAME),
                    config.getArrayValue(ConfigKey.KEY_DEVELOP_DATA, "")), new ModuleConfig(), this);
        } else if (message instanceof AMModule amModule) {
            if (agent == null) {
                throw new IllegalStateException("Agent not found. Make sure agent has been registered.");
            }
            Class<?> clazz = agent.registerModule(amModule.getModuleID(), amModule.getModuleName(), amModule.getDefaultClassName());
            String class_name = "";
            if (clazz != null) {
                class_name = clazz.getName();
            }
            MAModuleResponse maModuleResponse = new MAModuleResponse(amModule.getModuleID(), class_name);
            sendMessage(maModuleResponse);
        } else if (message instanceof AMUpdate amUpdate) {
            if (agent == null) {
                changeSetTemp.put(amUpdate.getTime(), amUpdate.getChanged());
                heardTemp.put(amUpdate.getTime(), amUpdate.getHeard());
                return;
            }
            if (!changeSetTemp.isEmpty() && !heardTemp.isEmpty()) {
                for (int i = 1; i < amUpdate.getTime(); i++) {
                    agent.update(i, changeSetTemp.get(i), heardTemp.get(i));
                }
                changeSetTemp.clear();
                heardTemp.clear();
            }
            agent.update(amUpdate.getTime(), amUpdate.getChanged(), amUpdate.getHeard());
        } else if (message instanceof AMExec amExec) {
            Config result = agent.execModuleMethod(amExec.getModuleID(), amExec.getMethodName(), amExec.getArguments());
            MAExecResponse maExecResponse = new MAExecResponse(amExec.getModuleID(), result);
            sendMessage(maExecResponse);
        }
    }

    private MessageProto receiveMessage() {
        try {
            int size = EncodingTools.readInt32(inputStream);
            byte[] bytes = inputStream.readNBytes(size);
            return MessageProto.parseFrom(bytes);
        } catch (IOException ignored) {
        }
        return null;
    }

    private void sendMessage(MessageProto messageProto) {
        try {
            byte[] bytes = messageProto.toByteArray();
            EncodingTools.writeInt32(bytes.length, outputStream);
            outputStream.write(bytes);
            outputStream.flush();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public void sendMessage(Message message) {
        sendMessage(message.toMessageProto());
    }

    public void shutdown() {
        running = false;
    }
}
