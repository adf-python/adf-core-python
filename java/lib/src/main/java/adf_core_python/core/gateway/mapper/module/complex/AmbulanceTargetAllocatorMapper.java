package adf_core_python.core.gateway.mapper.module.complex;

import adf_core_python.core.agent.communication.MessageManager;
import adf_core_python.core.agent.precompute.PrecomputeData;
import adf_core_python.core.component.module.complex.AmbulanceTargetAllocator;

public class AmbulanceTargetAllocatorMapper extends TargetAllocatorMapper {
    public AmbulanceTargetAllocatorMapper(AmbulanceTargetAllocator ambulanceTargetAllocator, PrecomputeData precomputeData, MessageManager messageManager) {
        super(ambulanceTargetAllocator, precomputeData, messageManager);
        this.targetClass = AmbulanceTargetAllocator.class;
    }
}
