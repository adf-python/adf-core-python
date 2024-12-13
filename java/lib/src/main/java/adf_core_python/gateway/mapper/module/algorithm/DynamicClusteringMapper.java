package adf_core_python.gateway.mapper.module.algorithm;

import adf.core.agent.communication.MessageManager;
import adf.core.agent.info.WorldInfo;
import adf_core_python.agent.precompute.PrecomputeData;
import adf_core_python.component.module.algorithm.DynamicClustering;

public class DynamicClusteringMapper extends ClusteringMapper {
    public DynamicClusteringMapper(DynamicClustering dynamicClustering, PrecomputeData precomputeData, MessageManager messageManager, WorldInfo worldInfo) {
        super(dynamicClustering, precomputeData, messageManager, worldInfo);
    }
}
