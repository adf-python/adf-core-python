package adf_core_python.core.gateway.mapper.module.complex;

import adf_core_python.core.agent.communication.MessageManager;
import adf_core_python.core.agent.precompute.PrecomputeData;
import adf_core_python.core.component.module.complex.BuildingDetector;

public class BuildingDetectorMapper extends TargetDetectorMapper {
    public BuildingDetectorMapper(BuildingDetector buildingDetector, PrecomputeData precomputeData, MessageManager messageManager) {
        super(buildingDetector, precomputeData, messageManager);
        this.targetClass = BuildingDetector.class;
    }
}
