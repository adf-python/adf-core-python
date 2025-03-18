package adf_core_python.core.gateway.mapper.module.complex;

import adf_core_python.core.agent.communication.MessageManager;
import adf_core_python.core.agent.precompute.PrecomputeData;
import adf_core_python.core.component.module.complex.PoliceTargetAllocator;

public class PoliceTargetAllocatorMapper extends TargetAllocatorMapper {
    public PoliceTargetAllocatorMapper(PoliceTargetAllocator policeTargetAllocator, PrecomputeData precomputeData, MessageManager messageManager) {
        super(policeTargetAllocator, precomputeData, messageManager);
        this.targetClass = PoliceTargetAllocator.class;
    }
}
