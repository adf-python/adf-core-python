from typing import Optional


class ModuleDict:
  def __init__(self, module_dict: Optional[dict[str, str]] = None):
    self.module_dict: dict[str, str] = {
      "adf_core_python.component.module.algorithm.Clustering": "adf_core_python.core.gateway.component.module.complex.gateway_clustering.GatewayClustering",
      "adf_core_python.component.module.algorithm.DynamicClustering": "adf_core_python.core.gateway.component.module.complex.gateway_clustering.GatewayClustering",
      "adf_core_python.component.module.algorithm.StaticClustering": "adf_core_python.core.gateway.component.module.complex.gateway_clustering.GatewayClustering",
      "adf_core_python.component.module.algorithm.PathPlanning": "adf_core_python.core.gateway.component.module.complex.gateway_path_planning.GatewayPathPlanning",
      "adf_core_python.component.module.complex.TargetDetector": "adf_core_python.core.gateway.component.module.complex.gateway_target_detector.GatewayTargetDetector",
      "adf_core_python.component.module.complex.HumanDetector": "adf_core_python.core.gateway.component.module.complex.gateway_human_detector.GatewayHumanDetector",
      "adf_core_python.component.module.complex.RoadDetector": "adf_core_python.core.gateway.component.module.complex.gateway_road_detector.GatewayRoadDetector",
      "adf_core_python.component.module.complex.Search": "adf_core_python.core.gateway.component.module.complex.gateway_search.GatewaySearch",
      "adf_core_python.component.module.complex.TargetAllocator": "adf_core_python.core.gateway.component.module.complex.gateway_target_allocator.GatewayTargetAllocator",
      "adf_core_python.component.module.complex.AmbulanceTargetAllocator": "adf_core_python.core.gateway.component.module.complex.gateway_ambulance_target_allocator.GatewayAmbulanceTargetAllocator",
      "adf_core_python.component.module.complex.FireTargetAllocator": "adf_core_python.core.gateway.component.module.complex.gateway_fire_target_allocator.GatewayFireTargetAllocator",
      "adf_core_python.component.module.complex.PoliceTargetAllocator": "adf_core_python.core.gateway.component.module.complex.gateway_fire_target_allocator.GatewayPoliceTargetAllocator",
    }
    if module_dict is not None:
      for key, value in module_dict.items():
        self.module_dict[key] = value

  def __getitem__(self, key: str) -> Optional[str]:
    if not isinstance(key, str):
      raise TypeError("TypeError: Key must be a string")
    return self.module_dict.get(key)

  def __setitem__(self, key: str, value: str) -> None:
    if not isinstance(key, str):
      raise TypeError("TypeError: Key must be a string")
    self.module_dict[key] = value
