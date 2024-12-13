package adf_core_python.agent;

import adf.core.agent.communication.MessageManager;
import adf.core.agent.info.ScenarioInfo;
import adf.core.agent.info.WorldInfo;
import adf_core_python.agent.config.ModuleConfig;
import adf_core_python.agent.develop.DevelopData;
import adf_core_python.agent.info.AgentInfo;
import adf_core_python.agent.module.ModuleManager;
import adf_core_python.agent.precompute.PrecomputeData;
import adf_core_python.component.module.AbstractModule;
import adf_core_python.gateway.mapper.AbstractMapper;
import adf_core_python.gateway.mapper.MapperDict;
import jakarta.annotation.Nonnull;
import jakarta.annotation.Nullable;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import rescuecore2.config.Config;
import rescuecore2.messages.Command;
import rescuecore2.standard.entities.StandardEntityURN;
import rescuecore2.standard.entities.StandardWorldModel;
import rescuecore2.worldmodel.ChangeSet;
import rescuecore2.worldmodel.Entity;
import rescuecore2.worldmodel.EntityID;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.util.Collection;
import java.util.HashMap;
import java.util.Objects;

public class Agent {
    private final AgentInfo agentInfo;
    private final WorldInfo worldInfo;
    private final ScenarioInfo scenarioInfo;
    private final ModuleManager moduleManager;
    private final DevelopData developData;
    private final PrecomputeData precomputeData;
    private final MessageManager messageManager;
    private final HashMap<String, AbstractMapper> modules = new HashMap<>();
    private final MapperDict mapperDict;
    private final Logger logger;

    public Agent(EntityID entityID, Collection<Entity> entities, ScenarioInfo scenarioInfo, DevelopData developData, ModuleConfig moduleConfig) {
        StandardWorldModel worldModel = new StandardWorldModel();
        worldModel.addEntities(entities);
        worldModel.index();

        this.agentInfo = new AgentInfo(entityID, worldModel);
        this.worldInfo = new WorldInfo(worldModel);
        this.scenarioInfo = scenarioInfo;
        this.developData = developData;
        this.moduleManager = new ModuleManager(this.agentInfo, this.worldInfo, this.scenarioInfo, moduleConfig, this.developData);

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
        agentInfo.recordThinkStartTime();
        agentInfo.setTime(time);
        agentInfo.setHeard(heard);
        agentInfo.setChanged(changed);
        worldInfo.setTime(time);
        worldInfo.merge(changed);
        worldInfo.setChanged(changed);
        logger.debug("Agent Update (Time: {}, Changed: {}, Heard: {})", agentInfo.getTime(), agentInfo.getChanged(), agentInfo.getHeard());
    }

    public Config execModuleMethod(String moduleID, String methodName, Config arguments) {
        logger.debug("Executing Method (MethodName: {}, Arguments: {}", methodName, arguments);
        Config result = modules.get(moduleID).execMethod(methodName, arguments);
        logger.debug("Executed Method Result (MethodName: {}, Result: {}", methodName, result);
        return result;
    }
}
