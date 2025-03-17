package adf_core_python.agent;

import adf.core.agent.communication.standard.bundle.StandardMessageBundle;
import adf.core.agent.info.ScenarioInfo;
import adf.core.agent.info.WorldInfo;
import adf.core.launcher.ConsoleOutput;
import adf_core_python.agent.communication.MessageManager;
import adf_core_python.agent.communication.standard.StandardCommunicationModule;
import adf_core_python.agent.config.ModuleConfig;
import adf_core_python.agent.develop.DevelopData;
import adf_core_python.agent.info.AgentInfo;
import adf_core_python.agent.module.ModuleManager;
import adf_core_python.agent.precompute.PrecomputeData;
import adf_core_python.component.communication.CommunicationModule;
import adf_core_python.component.module.AbstractModule;
import adf_core_python.gateway.Coordinator;
import adf_core_python.gateway.mapper.AbstractMapper;
import adf_core_python.gateway.mapper.MapperDict;
import jakarta.annotation.Nonnull;
import jakarta.annotation.Nullable;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import rescuecore2.config.Config;
import rescuecore2.messages.Command;
import rescuecore2.messages.Message;
import rescuecore2.standard.entities.StandardEntityURN;
import rescuecore2.standard.entities.StandardWorldModel;
import rescuecore2.standard.messages.AKSubscribe;
import rescuecore2.worldmodel.ChangeSet;
import rescuecore2.worldmodel.Entity;
import rescuecore2.worldmodel.EntityID;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.Objects;

public class Agent {
    public final AgentInfo agentInfo;
    public final WorldInfo worldInfo;
    public final ScenarioInfo scenarioInfo;
    private final ModuleManager moduleManager;
    private final DevelopData developData;
    private final PrecomputeData precomputeData;
    private final MessageManager messageManager;
    private CommunicationModule communicationModule;
    private final HashMap<String, AbstractMapper> modules = new HashMap<>();
    private final MapperDict mapperDict;
    private final Logger logger;
    private int ignoreTime;
    private final Coordinator coordinator;

    public Agent(EntityID entityID, Collection<Entity> entities, ScenarioInfo scenarioInfo, DevelopData developData, ModuleConfig moduleConfig, Coordinator coordinator) {
        StandardWorldModel worldModel = new StandardWorldModel();
        worldModel.addEntities(entities);
        worldModel.index();

        this.ignoreTime = scenarioInfo.getRawConfig()
                .getIntValue(kernel.KernelConstants.IGNORE_AGENT_COMMANDS_KEY);

        this.agentInfo = new AgentInfo(entityID, worldModel);
        this.worldInfo = new WorldInfo(worldModel);
        this.scenarioInfo = scenarioInfo;
        this.developData = developData;
        this.moduleManager = new ModuleManager(this.agentInfo, this.worldInfo, this.scenarioInfo, moduleConfig, this.developData);
        this.coordinator = coordinator;

        String dataStorageName = "";
        StandardEntityURN agentURN = Objects.requireNonNull(this.worldInfo.getEntity(this.agentInfo.getID())).getStandardURN();
        if (agentURN == StandardEntityURN.AMBULANCE_TEAM || agentURN == StandardEntityURN.AMBULANCE_CENTRE) {
            dataStorageName = "ambulance.bin";
        }
        if (agentURN == StandardEntityURN.FIRE_BRIGADE || agentURN == StandardEntityURN.FIRE_STATION) {
            dataStorageName = "fire.bin";
        }
        if (agentURN == StandardEntityURN.POLICE_FORCE || agentURN == StandardEntityURN.POLICE_OFFICE) {
            dataStorageName = "police.bin";
        }

        this.precomputeData = new PrecomputeData(dataStorageName);
        this.messageManager = new MessageManager();

        this.mapperDict = new MapperDict();

        logger = LogManager.getLogger(this.getClass());
        logger.debug("New Agent Created (EntityID: {}, All Entities: {})", this.agentInfo.getID(), this.worldInfo.getAllEntities());
    }

    public Class<?> registerModule(@Nonnull String moduleID, @Nonnull String moduleName, @Nullable String defaultClassName) {
        AbstractModule abstractModule = moduleManager.getModule(moduleName, defaultClassName);
        if (abstractModule == null) return null;
        Class<?> clazz = abstractModule.getClass();
        while (clazz.getSuperclass() != null) {
            if (mapperDict.getMapper(clazz) != null) {
                Class<? extends AbstractMapper> mapperClass = mapperDict.getMapper(clazz);
                try {
                    Constructor<? extends AbstractMapper> constructor = mapperClass.getConstructor(clazz, precomputeData.getClass(), messageManager.getClass());
                    AbstractMapper mapperInstance = constructor.newInstance(abstractModule, precomputeData, messageManager);
                    modules.put(moduleID, mapperInstance);
                    logger.debug("Registered Human Detector (ModuleID: {}, Instance: {})", moduleID, modules.get(moduleID));
                    return mapperInstance.getTargetClass();
                } catch (InstantiationException | IllegalAccessException | NoSuchMethodException |
                         InvocationTargetException e) {
                    throw new RuntimeException(e);
                }
            }
            clazz = clazz.getSuperclass();
        }
        return null;
    }

    public void update(int time, ChangeSet changed, Collection<Command> heard) {
        worldInfo.setTime(time);
        worldInfo.merge(changed);
        agentInfo.recordThinkStartTime();
        agentInfo.setTime(time);

        if (time == 1) {
            if (this.communicationModule != null) {
                ConsoleOutput.out(ConsoleOutput.State.ERROR,
                        "[ERROR ] Loader is not found.");
                ConsoleOutput.out(ConsoleOutput.State.NOTICE,
                        "CommunicationModule is modified - " + this);
            } else {
                this.communicationModule = new StandardCommunicationModule();
            }

            this.messageManager.registerMessageBundle(new StandardMessageBundle());
        }

        // agents can subscribe after ignore time
        if (time >= ignoreTime) {
            this.messageManager.subscribe(this.agentInfo, this.worldInfo,
                    this.scenarioInfo);

            if (!this.messageManager.getIsSubscribed()) {
                int[] channelsToSubscribe = this.messageManager.getChannels();
                if (channelsToSubscribe != null) {
                    this.messageManager.setIsSubscribed(true);
                }
            }
        }

        agentInfo.setHeard(heard);
        agentInfo.setChanged(changed);
        worldInfo.setChanged(changed);

        this.messageManager.refresh();
        this.communicationModule.receive(this, this.messageManager);

        this.messageManager.coordinateMessages(this.agentInfo, this.worldInfo,
                this.scenarioInfo);
        this.communicationModule.send(this, this.messageManager);

        logger.debug("Agent Update (Time: {}, Changed: {}, Heard: {})", agentInfo.getTime(), agentInfo.getChanged(), agentInfo.getHeard());
    }

    public Config execModuleMethod(String moduleID, String methodName, Config arguments) {
        logger.debug("Executing Method (MethodName: {}, Arguments: {}", methodName, arguments);
        Config result = modules.get(moduleID).execMethod(methodName, arguments);
        logger.debug("Executed Method Result (MethodName: {}, Result: {}", methodName, result);
        return result;
    }

    public EntityID getID() {
        return this.agentInfo.getID();
    }

    public void send(Message[] messages) {
        Arrays.stream(messages).forEach(coordinator::sendMessage);
    }
}
