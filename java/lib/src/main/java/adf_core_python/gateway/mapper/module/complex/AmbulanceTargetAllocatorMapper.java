package adf_core_python.gateway.mapper.module.complex;

import adf.core.agent.communication.MessageManager;
import adf_core_python.agent.precompute.PrecomputeData;
import adf_core_python.component.module.complex.AmbulanceTargetAllocator;

public class AmbulanceTargetAllocatorMapper extends TargetAllocatorMapper {
    public AmbulanceTargetAllocatorMapper(AmbulanceTargetAllocator ambulanceTargetAllocator, PrecomputeData precomputeData, MessageManager messageManager) {
        super(ambulanceTargetAllocator, precomputeData, messageManager);
        this.targetClass = AmbulanceTargetAllocator.class;
    }
}
