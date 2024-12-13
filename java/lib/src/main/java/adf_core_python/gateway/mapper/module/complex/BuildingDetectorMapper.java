package adf_core_python.gateway.mapper.module.complex;

import adf.core.agent.communication.MessageManager;
import adf_core_python.agent.precompute.PrecomputeData;
import adf_core_python.component.module.complex.BuildingDetector;

public class BuildingDetectorMapper extends TargetDetectorMapper {
    public BuildingDetectorMapper(BuildingDetector buildingDetector, PrecomputeData precomputeData, MessageManager messageManager) {
        super(buildingDetector, precomputeData, messageManager);
        this.targetClass = BuildingDetector.class;
    }
}
