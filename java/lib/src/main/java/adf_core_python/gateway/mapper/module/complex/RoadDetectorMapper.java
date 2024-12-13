package adf_core_python.gateway.mapper.module.complex;

import adf.core.agent.communication.MessageManager;
import adf_core_python.agent.precompute.PrecomputeData;
import adf_core_python.component.module.complex.RoadDetector;

public class RoadDetectorMapper extends TargetDetectorMapper {
    public RoadDetectorMapper(RoadDetector roadDetector, PrecomputeData precomputeData, MessageManager messageManager) {
        super(roadDetector, precomputeData, messageManager);
        this.targetClass = RoadDetector.class;
    }
}
