package adf_core_python.gateway.mapper.module.complex;

import adf.core.agent.communication.MessageManager;
import adf_core_python.agent.precompute.PrecomputeData;
import adf_core_python.component.module.complex.Search;

public class SearchMapper extends TargetDetectorMapper {
    public SearchMapper(Search search, PrecomputeData precomputeData, MessageManager messageManager) {
        super(search, precomputeData, messageManager);
    }
}
