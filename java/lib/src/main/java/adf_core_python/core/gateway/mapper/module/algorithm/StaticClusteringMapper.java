package adf_core_python.core.gateway.mapper.module.algorithm;

import adf.core.agent.info.WorldInfo;
import adf_core_python.core.agent.communication.MessageManager;
import adf_core_python.core.agent.precompute.PrecomputeData;
import adf_core_python.core.component.module.algorithm.StaticClustering;

public class StaticClusteringMapper extends ClusteringMapper {
    public StaticClusteringMapper(StaticClustering staticClustering, PrecomputeData precomputeData, MessageManager messageManager, WorldInfo worldInfo) {
        super(staticClustering, precomputeData, messageManager, worldInfo);
    }
}
