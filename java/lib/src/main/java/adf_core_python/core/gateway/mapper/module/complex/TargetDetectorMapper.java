package adf_core_python.core.gateway.mapper.module.complex;

import adf_core_python.core.agent.communication.MessageManager;
import adf_core_python.core.agent.precompute.PrecomputeData;
import adf_core_python.core.component.module.complex.TargetDetector;
import adf_core_python.core.gateway.mapper.module.AbstractModuleMapper;
import rescuecore2.config.Config;
import rescuecore2.worldmodel.EntityID;

public class TargetDetectorMapper extends AbstractModuleMapper {
    public TargetDetectorMapper(TargetDetector targetDetector, PrecomputeData precomputeData, MessageManager messageManager) {
        super(targetDetector, precomputeData, messageManager);
        this.targetClass = TargetDetector.class;
    }

    @Override
    public Config execMethod(String methodName, Config arguments) {
        Config result = super.execMethod(methodName, arguments);
        if (methodName.equals("getTarget")) {
            result = execGetTarget();
        }
        return result;
    }

    public Config execGetTarget() {
        TargetDetector targetDetector = (TargetDetector) abstractModule;
        EntityID entityID = targetDetector.getTarget();
        Config result = new Config();
        result.setIntValue("EntityID", -1);
        if (entityID != null) {
            result.setIntValue("EntityID", entityID.getValue());
        }
        return result;
    }
}
