package adf_core_python.gateway.mapper.module.complex;

import adf.core.agent.communication.MessageManager;
import adf_core_python.agent.precompute.PrecomputeData;
import adf_core_python.component.module.complex.PoliceTargetAllocator;

public class PoliceTargetAllocatorMapper extends TargetAllocatorMapper {
    public PoliceTargetAllocatorMapper(PoliceTargetAllocator policeTargetAllocator, PrecomputeData precomputeData, MessageManager messageManager) {
        super(policeTargetAllocator, precomputeData, messageManager);
        this.targetClass = PoliceTargetAllocator.class;
    }
}
