package adf_core_python.core.component.module.complex;

import adf.core.agent.develop.DevelopData;
import adf.core.agent.info.ScenarioInfo;
import adf.core.agent.info.WorldInfo;
import adf_core_python.core.agent.communication.MessageManager;
import adf_core_python.core.agent.info.AgentInfo;
import adf_core_python.core.agent.module.ModuleManager;
import adf_core_python.core.agent.precompute.PrecomputeData;
import adf_core_python.core.component.module.AbstractModule;
import rescuecore2.standard.entities.StandardEntity;
import rescuecore2.worldmodel.EntityID;

public abstract class TargetDetector<E extends StandardEntity>
        extends AbstractModule {

    public TargetDetector(AgentInfo ai, WorldInfo wi, ScenarioInfo si, ModuleManager moduleManager, DevelopData developData) {
        super(ai, wi, si, moduleManager, developData);
    }


    public abstract EntityID getTarget();

    @Override
    public abstract TargetDetector<E> calc();


    @Override
    public TargetDetector<E> precompute(PrecomputeData precomputeData) {
        super.precompute(precomputeData);
        return this;
    }


    @Override
    public TargetDetector<E> resume(PrecomputeData precomputeData) {
        super.resume(precomputeData);
        return this;
    }


    @Override
    public TargetDetector<E> preparate() {
        super.preparate();
        return this;
    }


    @Override
    public TargetDetector<E> updateInfo(MessageManager messageManager) {
        super.updateInfo(messageManager);
        return this;
    }
}
