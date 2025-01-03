package adf_core_python.gateway.mapper.module.algorithm;

import java.util.Collection;
import java.util.List;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;

import adf.core.agent.communication.MessageManager;
import adf_core_python.agent.precompute.PrecomputeData;
import adf_core_python.component.module.algorithm.PathPlanning;
import adf_core_python.gateway.mapper.module.AbstractModuleMapper;
import rescuecore2.config.Config;
import rescuecore2.worldmodel.EntityID;

public class PathPlanningMapper extends AbstractModuleMapper {
    public PathPlanningMapper(PathPlanning pathPlanning, PrecomputeData precomputeData, MessageManager messageManager) {
        super(pathPlanning, precomputeData, messageManager);
    }

    @Override
    public Config execMethod(String methodName, Config arguments) {
        Config result = super.execMethod(methodName, arguments);
        if (methodName.equals("getResult")) {
            result = execGetResult();
        }
        if (methodName.equals("setFrom(EntityID)")) {
            execSetFrom(new EntityID(arguments.getIntValue("EntityID")));
        }
        if (methodName.equals("setDestination(Collection<EntityID>)")) {
            ObjectMapper objectMapper = new ObjectMapper();
            Collection<EntityID> targets;
            try {
                targets = objectMapper.readValue(arguments.getValue("Targets"), new TypeReference<List<EntityID>>() {
                });
            } catch (JsonProcessingException e) {
                throw new RuntimeException(e);
            }
            execSetDestination(targets);
        }
        if (methodName.equals("getDistance")) {
            result = execGetDistance();
        }
        if (methodName.equals("getDistance(EntityID, EntityID)")) {
            result = execGetDistance(new EntityID(arguments.getIntValue("From")),
                    new EntityID(arguments.getIntValue("Dest")));
        }
        if (methodName.equals("getResult(EntityID, EntityID)")) {
            result = execGetResult(new EntityID(arguments.getIntValue("From")),
                    new EntityID(arguments.getIntValue("Dest")));
        }
        if (methodName.equals("getResult(EntityID, List[EntityID])")) {
            ObjectMapper objectMapper = new ObjectMapper();
            Collection<EntityID> destinations;
            try {
                destinations = objectMapper.readValue(arguments.getValue("Destinations"),
                        new TypeReference<List<EntityID>>() {
                        });
            } catch (JsonProcessingException e) {
                throw new RuntimeException(e);
            }
            result = execGetResult(new EntityID(arguments.getIntValue("From")), destinations);
        }
        return result;
    }

    private Config execGetResult() {
        PathPlanning pathPlanning = (PathPlanning) abstractModule;
        List<EntityID> entityIDs = pathPlanning.getResult();
        ObjectMapper objectMapper = new ObjectMapper();
        String jsonStr;
        try {
            jsonStr = objectMapper.writeValueAsString(entityIDs);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
        Config result = new Config();
        result.setValue("EntityIDs", jsonStr);
        return result;
    }

    private void execSetFrom(EntityID entityID) {
        PathPlanning pathPlanning = (PathPlanning) abstractModule;
        pathPlanning.setFrom(entityID);
    }

    private void execSetDestination(Collection<EntityID> targets) {
        PathPlanning pathPlanning = (PathPlanning) abstractModule;
        pathPlanning.setDestination(targets);
    }

    private Config execGetDistance() {
        PathPlanning pathPlanning = (PathPlanning) abstractModule;
        Double distance = pathPlanning.getDistance();
        Config result = new Config();
        result.setValue("Distance", String.valueOf(distance));
        return result;
    }

    private Config execGetDistance(EntityID from, EntityID dest) {
        PathPlanning pathPlanning = (PathPlanning) abstractModule;
        Double distance = pathPlanning.getDistance(from, dest);
        Config result = new Config();
        result.setValue("Distance", String.valueOf(distance));
        return result;
    }

    private Config execGetResult(EntityID from, EntityID dest) {
        PathPlanning pathPlanning = (PathPlanning) abstractModule;
        List<EntityID> entityIDs = pathPlanning.getResult(from, dest);
        Config result = new Config();
        ObjectMapper objectMapper = new ObjectMapper();
        String jsonStr;
        try {
            jsonStr = objectMapper.writeValueAsString(entityIDs.stream().map(EntityID::getValue).toArray());
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
        result.setValue("Result", String.valueOf(jsonStr));
        return result;
    }

    private Config execGetResult(EntityID from, Collection<EntityID> destinations) {
        PathPlanning pathPlanning = (PathPlanning) abstractModule;
        pathPlanning.setFrom(from);
        pathPlanning.setDestination(destinations);
        List<EntityID> entityIDs = pathPlanning.getResult();
        Config result = new Config();
        ObjectMapper objectMapper = new ObjectMapper();
        String jsonStr;
        try {
            jsonStr = objectMapper.writeValueAsString(entityIDs.stream().map(EntityID::getValue).toArray());
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
        result.setValue("Result", String.valueOf(jsonStr));
        return result;
    }
}
