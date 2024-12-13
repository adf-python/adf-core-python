package adf_core_python.gateway.mapper;

import adf_core_python.component.module.AbstractModule;
import adf_core_python.component.module.algorithm.Clustering;
import adf_core_python.component.module.algorithm.DynamicClustering;
import adf_core_python.component.module.algorithm.PathPlanning;
import adf_core_python.component.module.algorithm.StaticClustering;
import adf_core_python.component.module.complex.*;
import adf_core_python.gateway.mapper.module.AbstractModuleMapper;
import adf_core_python.gateway.mapper.module.algorithm.ClusteringMapper;
import adf_core_python.gateway.mapper.module.algorithm.DynamicClusteringMapper;
import adf_core_python.gateway.mapper.module.algorithm.PathPlanningMapper;
import adf_core_python.gateway.mapper.module.algorithm.StaticClusteringMapper;
import adf_core_python.gateway.mapper.module.complex.*;

import java.util.HashMap;

public class MapperDict {
    private final HashMap<Class<?>, Class<? extends AbstractMapper>> mapperDict;

    public MapperDict() {
        mapperDict = new HashMap<>();
        registerMapper(Clustering.class, ClusteringMapper.class);
        registerMapper(DynamicClustering.class, DynamicClusteringMapper.class);
        registerMapper(StaticClustering.class, StaticClusteringMapper.class);

        registerMapper(PathPlanning.class, PathPlanningMapper.class);

        registerMapper(TargetDetector.class, TargetDetectorMapper.class);
        registerMapper(HumanDetector.class, HumanDetectorMapper.class);
        registerMapper(RoadDetector.class, RoadDetectorMapper.class);
        registerMapper(BuildingDetector.class, BuildingDetectorMapper.class);

        registerMapper(Search.class, SearchMapper.class);

        registerMapper(TargetAllocator.class, TargetAllocatorMapper.class);
        registerMapper(AmbulanceTargetAllocator.class, AmbulanceTargetAllocatorMapper.class);
        registerMapper(FireTargetAllocator.class, FireTargetAllocatorMapper.class);
        registerMapper(PoliceTargetAllocator.class, PoliceTargetAllocatorMapper.class);

        registerMapper(AbstractModule.class, AbstractModuleMapper.class);
    }

    public void registerMapper(Class<?> component, Class<? extends AbstractMapper> mapper) {
        mapperDict.put(component, mapper);
    }

    public Class<? extends AbstractMapper> getMapper(Class<?> component) {
        return mapperDict.get(component);
    }
}
