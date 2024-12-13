package adf_core_python.component.module.complex;

import adf.core.agent.communication.MessageManager;
import adf.core.agent.info.ScenarioInfo;
import adf.core.agent.info.WorldInfo;
import adf_core_python.agent.develop.DevelopData;
import adf_core_python.agent.info.AgentInfo;
import adf_core_python.agent.module.ModuleManager;
import adf_core_python.agent.precompute.PrecomputeData;
import rescuecore2.standard.entities.Road;

public abstract class RoadDetector extends TargetDetector<Road> {

    public RoadDetector(AgentInfo ai, WorldInfo wi, ScenarioInfo si, ModuleManager moduleManager, DevelopData developData) {
        super(ai, wi, si, moduleManager, developData);
    }


    @Override
    public RoadDetector precompute(PrecomputeData precomputeData) {
        super.precompute(precomputeData);
        return this;
    }


    @Override
    public RoadDetector resume(PrecomputeData precomputeData) {
        super.resume(precomputeData);
        return this;
    }


    @Override
    public RoadDetector preparate() {
        super.preparate();
        return this;
    }


    @Override
    public RoadDetector updateInfo(MessageManager messageManager) {
        super.updateInfo(messageManager);
        return this;
    }


    @Override
    public abstract RoadDetector calc();
}
