package adf_core_python.core.component.module.complex;

import adf.core.agent.develop.DevelopData;
import adf.core.agent.info.ScenarioInfo;
import adf.core.agent.info.WorldInfo;
import adf_core_python.core.agent.communication.MessageManager;
import adf_core_python.core.agent.info.AgentInfo;
import adf_core_python.core.agent.module.ModuleManager;
import adf_core_python.core.agent.precompute.PrecomputeData;
import rescuecore2.standard.entities.Area;

public abstract class Search extends TargetDetector<Area> {

    public Search(AgentInfo ai, WorldInfo wi, ScenarioInfo si, ModuleManager moduleManager, DevelopData developData) {
        super(ai, wi, si, moduleManager, developData);
    }


    @Override
    public Search precompute(PrecomputeData precomputeData) {
        super.precompute(precomputeData);
        return this;
    }


    @Override
    public Search resume(PrecomputeData precomputeData) {
        super.resume(precomputeData);
        return this;
    }


    @Override
    public Search preparate() {
        super.preparate();
        return this;
    }


    @Override
    public Search updateInfo(MessageManager messageManager) {
        super.updateInfo(messageManager);
        return this;
    }


    @Override
    public abstract Search calc();
}
