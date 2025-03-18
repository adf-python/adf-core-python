package adf_core_python.core.gateway.mapper.module.complex;

import adf_core_python.core.agent.communication.MessageManager;
import adf_core_python.core.agent.precompute.PrecomputeData;
import adf_core_python.core.component.module.complex.FireTargetAllocator;

public class FireTargetAllocatorMapper extends TargetAllocatorMapper {
    public FireTargetAllocatorMapper(FireTargetAllocator fireTargetAllocator, PrecomputeData precomputeData, MessageManager messageManager) {
        super(fireTargetAllocator, precomputeData, messageManager);
        this.targetClass = FireTargetAllocator.class;
    }
}
