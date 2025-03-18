package adf_core_python.core.gateway.mapper.module.complex;

import adf_core_python.core.agent.communication.MessageManager;
import adf_core_python.core.agent.precompute.PrecomputeData;
import adf_core_python.core.component.module.complex.HumanDetector;

public class HumanDetectorMapper extends TargetDetectorMapper {
    public HumanDetectorMapper(HumanDetector humanDetector, PrecomputeData precomputeData, MessageManager messageManager) {
        super(humanDetector, precomputeData, messageManager);
        this.targetClass = HumanDetector.class;
    }
}
