package adf_core_python.core.gateway.mapper.module.complex;

import adf_core_python.core.agent.communication.MessageManager;
import adf_core_python.core.agent.precompute.PrecomputeData;
import adf_core_python.core.component.module.complex.RoadDetector;

public class RoadDetectorMapper extends TargetDetectorMapper {
    public RoadDetectorMapper(RoadDetector roadDetector, PrecomputeData precomputeData, MessageManager messageManager) {
        super(roadDetector, precomputeData, messageManager);
        this.targetClass = RoadDetector.class;
    }
}
