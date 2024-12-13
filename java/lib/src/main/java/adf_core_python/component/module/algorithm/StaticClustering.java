package adf_core_python.component.module.algorithm;

import adf.core.agent.info.ScenarioInfo;
import adf.core.agent.info.WorldInfo;
import adf_core_python.agent.develop.DevelopData;
import adf_core_python.agent.info.AgentInfo;
import adf_core_python.agent.module.ModuleManager;

public abstract class StaticClustering extends Clustering {

    public StaticClustering(AgentInfo ai, WorldInfo wi, ScenarioInfo si, ModuleManager moduleManager, DevelopData developData) {
        super(ai, wi, si, moduleManager, developData);
    }
}
