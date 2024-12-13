package adf_core_python.gateway.mapper.module.complex;

import adf.core.agent.communication.MessageManager;
import adf_core_python.agent.precompute.PrecomputeData;
import adf_core_python.component.module.complex.FireTargetAllocator;

public class FireTargetAllocatorMapper extends TargetAllocatorMapper {
    public FireTargetAllocatorMapper(FireTargetAllocator fireTargetAllocator, PrecomputeData precomputeData, MessageManager messageManager) {
        super(fireTargetAllocator, precomputeData, messageManager);
        this.targetClass = FireTargetAllocator.class;
    }
}
