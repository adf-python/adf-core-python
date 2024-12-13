package adf_core_python.gateway.mapper.module.complex;

import adf.core.agent.communication.MessageManager;
import adf_core_python.agent.precompute.PrecomputeData;
import adf_core_python.component.module.complex.HumanDetector;

public class HumanDetectorMapper extends TargetDetectorMapper {
    public HumanDetectorMapper(HumanDetector humanDetector, PrecomputeData precomputeData, MessageManager messageManager) {
        super(humanDetector, precomputeData, messageManager);
        this.targetClass = HumanDetector.class;
    }
}
