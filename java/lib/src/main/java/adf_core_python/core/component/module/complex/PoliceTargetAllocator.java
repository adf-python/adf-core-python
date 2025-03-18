package adf_core_python.core.component.module.complex;

import adf.core.agent.develop.DevelopData;
import adf.core.agent.info.ScenarioInfo;
import adf.core.agent.info.WorldInfo;
import adf_core_python.core.agent.communication.MessageManager;
import adf_core_python.core.agent.info.AgentInfo;
import adf_core_python.core.agent.module.ModuleManager;
import adf_core_python.core.agent.precompute.PrecomputeData;
import rescuecore2.worldmodel.EntityID;

import java.util.Map;

public abstract class PoliceTargetAllocator extends TargetAllocator {

    public PoliceTargetAllocator(AgentInfo ai, WorldInfo wi, ScenarioInfo si, ModuleManager moduleManager, DevelopData developData) {
        super(ai, wi, si, moduleManager, developData);
    }


    @Override
    public abstract Map<EntityID, EntityID> getResult();

    @Override
    public abstract PoliceTargetAllocator calc();


    @Override
    public PoliceTargetAllocator resume(PrecomputeData precomputeData) {
        super.resume(precomputeData);
        return this;
    }


    @Override
    public PoliceTargetAllocator preparate() {
        super.preparate();
        return this;
    }


    @Override
    public PoliceTargetAllocator updateInfo(MessageManager messageManager) {
        super.updateInfo(messageManager);
        return this;
    }
}
