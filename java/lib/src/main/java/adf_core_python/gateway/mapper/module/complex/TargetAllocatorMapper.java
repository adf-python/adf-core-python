package adf_core_python.gateway.mapper.module.complex;

import adf.core.agent.communication.MessageManager;
import adf_core_python.agent.precompute.PrecomputeData;
import adf_core_python.component.module.complex.TargetAllocator;
import adf_core_python.gateway.mapper.module.AbstractModuleMapper;
import rescuecore2.config.Config;
import rescuecore2.worldmodel.EntityID;

import java.util.Map;

public class TargetAllocatorMapper extends AbstractModuleMapper {
    public TargetAllocatorMapper(TargetAllocator targetAllocator, PrecomputeData precomputeData, MessageManager messageManager) {
        super(targetAllocator, precomputeData, messageManager);
        this.targetClass = TargetAllocator.class;
    }

    @Override
    public Config execMethod(String methodName, Config arguments) {
        Config result = super.execMethod(methodName, arguments);
        if (methodName.equals("getResult")) {
            result = execGetResult();
        }
        return result;
    }

    public Config execGetResult() {
        TargetAllocator targetAllocator = (TargetAllocator) abstractModule;
        Map<EntityID, EntityID> result = targetAllocator.getResult();
        Config response = new Config();
        result.forEach((k, v) -> response.setValue(String.valueOf(k.getValue()), String.valueOf(v.getValue())));
        return response;
    }
}
