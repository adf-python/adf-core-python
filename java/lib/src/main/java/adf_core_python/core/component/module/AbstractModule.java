package adf_core_python.core.component.module;

import adf.core.agent.develop.DevelopData;
import adf.core.agent.info.ScenarioInfo;
import adf.core.agent.info.WorldInfo;
import adf_core_python.core.agent.communication.MessageManager;
import adf_core_python.core.agent.info.AgentInfo;
import adf_core_python.core.agent.module.ModuleManager;
import adf_core_python.core.agent.precompute.PrecomputeData;

import java.util.ArrayList;
import java.util.List;

public abstract class AbstractModule {

    private final List<AbstractModule> subModules = new ArrayList<>();
    protected AgentInfo agentInfo;
    protected WorldInfo worldInfo;
    protected ScenarioInfo scenarioInfo;
    protected ModuleManager moduleManager;
    protected DevelopData developData;

    private int countPrecompute;
    private int countResume;
    private int countPreparate;
    private int countUpdateInfo;
    private int countUpdateInfoCurrentTime;

    public AbstractModule(AgentInfo agentInfo, WorldInfo worldInfo, ScenarioInfo scenarioInfo, ModuleManager moduleManager, DevelopData developData) {
        this.agentInfo = agentInfo;
        this.worldInfo = worldInfo;
        this.scenarioInfo = scenarioInfo;
        this.moduleManager = moduleManager;
        this.developData = developData;
        this.countPrecompute = 0;
        this.countResume = 0;
        this.countPreparate = 0;
        this.countUpdateInfo = 0;
        this.countUpdateInfoCurrentTime = 0;
    }


    protected void registerModule(AbstractModule module) {
        subModules.add(module);
    }


    protected boolean unregisterModule(AbstractModule module) {
        return subModules.remove(module);
    }


    public AbstractModule precompute(PrecomputeData precomputeData) {
        this.countPrecompute++;
        for (AbstractModule abstractModule : subModules) {
            abstractModule.precompute(precomputeData);
        }
        return this;
    }


    public AbstractModule resume(PrecomputeData precomputeData) {
        this.countResume++;
        for (AbstractModule abstractModule : subModules) {
            abstractModule.resume(precomputeData);
        }
        return this;
    }


    public AbstractModule preparate() {
        this.countPreparate++;
        for (AbstractModule abstractModule : subModules) {
            abstractModule.preparate();
        }
        return this;
    }


    public AbstractModule updateInfo(MessageManager messageManager) {
        if (this.countUpdateInfoCurrentTime != this.agentInfo.getTime()) {
            this.countUpdateInfo = 0;
            this.countUpdateInfoCurrentTime = this.agentInfo.getTime();
        }
        for (AbstractModule abstractModule : subModules) {
            abstractModule.updateInfo(messageManager);
        }
        this.countUpdateInfo++;
        return this;
    }


    public abstract AbstractModule calc();


    public int getCountPrecompute() {
        return this.countPrecompute;
    }


    public int getCountResume() {
        return this.countResume;
    }


    public int getCountPreparate() {
        return this.countPreparate;
    }


    public int getCountUpdateInfo() {
        if (this.countUpdateInfoCurrentTime != this.agentInfo.getTime()) {
            this.countUpdateInfo = 0;
            this.countUpdateInfoCurrentTime = this.agentInfo.getTime();
        }
        return this.countUpdateInfo;
    }


    public void resetCountPrecompute() {
        this.countPrecompute = 0;
    }


    public void resetCountResume() {
        this.countResume = 0;
    }


    public void resetCountPreparate() {
        this.countPreparate = 0;
    }


    public void resetCountUpdateInfo() {
        this.countUpdateInfo = 0;
    }
}
