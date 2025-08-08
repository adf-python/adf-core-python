package adf_core_python.core.gateway.mapper;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import rescuecore2.config.Config;

public abstract class AbstractMapper {
    protected Class<?> targetClass;
    protected Logger logger;

    public AbstractMapper() {
        this.targetClass = Object.class;
        logger = LogManager.getLogger(this.getClass());
    }

    public Class<?> getTargetClass() {
        return targetClass;
    }

    public abstract Config execMethod(String methodName, Config arguments);
}
