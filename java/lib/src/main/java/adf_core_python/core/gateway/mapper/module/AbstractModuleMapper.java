package adf_core_python.core.gateway.mapper.module;

import adf_core_python.core.agent.communication.MessageManager;
import adf_core_python.core.agent.precompute.PrecomputeData;
import adf_core_python.core.component.module.AbstractModule;
import adf_core_python.core.gateway.mapper.AbstractMapper;
import rescuecore2.config.Config;

public class AbstractModuleMapper extends AbstractMapper {
    protected final AbstractModule abstractModule;
    private final PrecomputeData precomputeData;
    private final MessageManager messageManager;

    public AbstractModuleMapper(AbstractModule abstractModule, PrecomputeData precomputeData, MessageManager messageManager) {
        super();
        this.targetClass = AbstractModule.class;
        this.abstractModule = abstractModule;
        this.precomputeData = precomputeData;
        this.messageManager = messageManager;
    }

    @Override
    public Config execMethod(String methodName, Config arguments) {
        switch (methodName) {
            case "precompute":
                execPrecompute();
                break;
            case "resume":
                execResume();
                break;
            case "preparate":
                execPreparate();
                break;
            case "updateInfo":
                execUpdateInfo();
                break;
            case "calc":
                execCalc();
                break;
        }

        return new Config();
    }

    public void execPrecompute() {
        abstractModule.precompute(precomputeData);
    }

    public void execResume() {
        abstractModule.resume(precomputeData);
    }

    public void execPreparate() {
        abstractModule.preparate();
    }

    public void execUpdateInfo() {
        abstractModule.updateInfo(messageManager);
    }

    public void execCalc() {
        abstractModule.calc();
    }
}
