package adf_core_python.core.gateway.mapper.module.algorithm;

import adf.core.agent.info.WorldInfo;
import adf_core_python.core.agent.communication.MessageManager;
import adf_core_python.core.agent.precompute.PrecomputeData;
import adf_core_python.core.component.module.algorithm.Clustering;
import adf_core_python.core.gateway.mapper.module.AbstractModuleMapper;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import rescuecore2.config.Config;
import rescuecore2.standard.entities.StandardEntity;
import rescuecore2.worldmodel.EntityID;

import java.util.Collection;
import java.util.List;
import java.util.stream.Collectors;

public class ClusteringMapper extends AbstractModuleMapper {
    private final WorldInfo worldInfo;

    public ClusteringMapper(Clustering clustering, PrecomputeData precomputeData, MessageManager messageManager, WorldInfo worldInfo) {
        super(clustering, precomputeData, messageManager);
        this.targetClass = Clustering.class;
        this.worldInfo = worldInfo;
    }

    @Override
    public Config execMethod(String methodName, Config arguments) {
        Config result = super.execMethod(methodName, arguments);
        if (methodName.equals("getClusterNumber")) {
            result = execGetClusterNumber();
        }
        if (methodName.equals("getClusterIndex(StandardEntity)")) {
            result = execGetClusterIndex(worldInfo.getEntity(new EntityID(arguments.getIntValue("EntityID"))));
        }
        if (methodName.equals("getClusterIndex(EntityID)")) {
            result = execGetClusterIndex(new EntityID(arguments.getIntValue("EntityID")));
        }
        if (methodName.equals("getClusterEntities(int)")) {
            result = execGetClusterEntities(arguments.getIntValue("Index"));
        }
        if (methodName.equals("getClusterEntityIDs(int)")) {
            result = execGetClusterEntityIDs(arguments.getIntValue("Index"));
        }
        if (methodName.equals("getAllClusterEntities")) {
            result = execGetAllClusterEntities();
        }
        if (methodName.equals("getAllClusterEntityIDs")) {
            result = execGetAllClusterEntityIDs();
        }
        return result;
    }

    private Config execGetClusterNumber() {
        Clustering clustering = (Clustering) abstractModule;
        int clusterNumber = clustering.getClusterNumber();
        Config result = new Config();
        result.setIntValue("ClusterNumber", clusterNumber);
        return result;
    }

    private Config execGetClusterIndex(StandardEntity standardEntity) {
        Clustering clustering = (Clustering) abstractModule;
        int clusterIndex = clustering.getClusterIndex(standardEntity);
        Config result = new Config();
        result.setIntValue("ClusterIndex", clusterIndex);
        return result;
    }

    private Config execGetClusterIndex(EntityID entityID) {
        Clustering clustering = (Clustering) abstractModule;
        int clusterIndex = clustering.getClusterIndex(entityID);
        Config result = new Config();
        result.setIntValue("ClusterIndex", clusterIndex);
        return result;
    }

    private Config execGetClusterEntities(int index) {
        Clustering clustering = (Clustering) abstractModule;
        Collection<StandardEntity> entities = clustering.getClusterEntities(index);
        ObjectMapper objectMapper = new ObjectMapper();
        String jsonStr = "";
        try {
            jsonStr = objectMapper.writeValueAsString(entities.stream().map(e -> e.getID().getValue()).toArray());
        } catch (JsonProcessingException ignored) {
        }
        Config result = new Config();
        result.setValue("EntityIDs", jsonStr);
        return result;
    }

    private Config execGetClusterEntityIDs(int index) {
        Clustering clustering = (Clustering) abstractModule;
        Collection<EntityID> entities = clustering.getClusterEntityIDs(index);
        ObjectMapper objectMapper = new ObjectMapper();
        String jsonStr = "";
        try {
            jsonStr = objectMapper.writeValueAsString(entities.stream().map(EntityID::getValue).toArray());
        } catch (JsonProcessingException ignored) {
        }
        Config result = new Config();
        result.setValue("EntityIDs", jsonStr);
        return result;
    }

    private Config execGetAllClusterEntities() {
        Clustering clustering = (Clustering) abstractModule;
        List<Collection<StandardEntity>> allClusterEntities = clustering.getAllClusterEntities();
        ObjectMapper objectMapper = new ObjectMapper();
        String jsonStr = "";
        try {
            jsonStr = objectMapper.writeValueAsString(allClusterEntities.stream().map(e -> e.stream().map(f -> f.getID().getValue()).collect(Collectors.toList())).toArray());
        } catch (JsonProcessingException ignored) {
        }
        Config result = new Config();
        result.setValue("EntityIDs", jsonStr);
        return result;
    }

    private Config execGetAllClusterEntityIDs() {
        Clustering clustering = (Clustering) abstractModule;
        List<Collection<EntityID>> allClusterEntityIDs = clustering.getAllClusterEntityIDs();
        ObjectMapper objectMapper = new ObjectMapper();
        String jsonStr = "";
        try {
            jsonStr = objectMapper.writeValueAsString(allClusterEntityIDs.stream().map(e -> e.stream().map(EntityID::getValue).collect(Collectors.toList())).toArray());
        } catch (JsonProcessingException ignored) {
        }
        Config result = new Config();
        result.setValue("EntityIDs", jsonStr);
        return result;
    }
}
