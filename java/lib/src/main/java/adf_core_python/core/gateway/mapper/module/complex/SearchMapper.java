package adf_core_python.core.gateway.mapper.module.complex;

import adf_core_python.core.agent.communication.MessageManager;
import adf_core_python.core.agent.precompute.PrecomputeData;
import adf_core_python.core.component.module.complex.Search;

public class SearchMapper extends TargetDetectorMapper {
    public SearchMapper(Search search, PrecomputeData precomputeData, MessageManager messageManager) {
        super(search, precomputeData, messageManager);
    }
}
