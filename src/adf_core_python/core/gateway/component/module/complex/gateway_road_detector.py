from __future__ import annotations

from typing import TYPE_CHECKING

from rcrscore.entities import Road

from adf_core_python.core.component.module.complex import RoadDetector
from adf_core_python.core.gateway.component.module.complex import (
  GatewayTargetDetector,
)

if TYPE_CHECKING:
  from adf_core_python.core.agent.communication import MessageManager
  from adf_core_python.core.agent.develop import DevelopData
  from adf_core_python.core.agent.info import AgentInfo, ScenarioInfo, WorldInfo
  from adf_core_python.core.agent.module import ModuleManager
  from adf_core_python.core.agent.precompute import PrecomputeData
  from adf_core_python.core.gateway import GatewayModule


class GatewayRoadDetector(GatewayTargetDetector[Road], RoadDetector):
  def __init__(
    self,
    agent_info: AgentInfo,
    world_info: WorldInfo,
    scenario_info: ScenarioInfo,
    module_manager: ModuleManager,
    develop_data: DevelopData,
    gateway_module: GatewayModule,
  ) -> None:
    super().__init__(
      agent_info,
      world_info,
      scenario_info,
      module_manager,
      develop_data,
      gateway_module,
    )

  def precompute(self, precompute_data: PrecomputeData) -> GatewayRoadDetector:
    super().precompute(precompute_data)
    return self

  def resume(self, precompute_data: PrecomputeData) -> GatewayRoadDetector:
    super().resume(precompute_data)
    return self

  def prepare(self) -> GatewayRoadDetector:
    super().prepare()
    return self

  def update_info(self, message_manager: MessageManager) -> GatewayRoadDetector:
    super().update_info(message_manager)
    return self

  def calculate(self) -> GatewayRoadDetector:
    super().calculate()
    return self
