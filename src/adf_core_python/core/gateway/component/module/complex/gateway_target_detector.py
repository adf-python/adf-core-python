from __future__ import annotations

from typing import TYPE_CHECKING, Generic, Optional, TypeVar

from rcrscore.entities import EntityID
from rcrscore.entities.entity import Entity

from adf_core_python.core.component.module.complex.target_detector import TargetDetector
from adf_core_python.core.gateway.component.module.gateway_abstract_module import (
  GatewayAbstractModule,
)

if TYPE_CHECKING:
  from adf_core_python.core.agent.communication.message_manager import MessageManager
  from adf_core_python.core.agent.develop.develop_data import DevelopData
  from adf_core_python.core.agent.info.agent_info import AgentInfo
  from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
  from adf_core_python.core.agent.info.world_info import WorldInfo
  from adf_core_python.core.agent.module.module_manager import ModuleManager
  from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData
  from adf_core_python.core.gateway.gateway_module import GatewayModule

T = TypeVar("T", bound=Entity)


class GatewayTargetDetector(GatewayAbstractModule, TargetDetector, Generic[T]):
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

  def precompute(self, precompute_data: PrecomputeData) -> GatewayTargetDetector[T]:
    super().precompute(precompute_data)
    return self

  def resume(self, precompute_data: PrecomputeData) -> GatewayTargetDetector[T]:
    super().resume(precompute_data)
    return self

  def prepare(self) -> GatewayTargetDetector[T]:
    super().prepare()
    return self

  def update_info(self, message_manager: MessageManager) -> GatewayTargetDetector[T]:
    super().update_info(message_manager)
    return self

  def calculate(self) -> GatewayTargetDetector[T]:
    super().calculate()
    return self

  def get_target_entity_id(self) -> Optional[EntityID]:
    result = self._gateway_module.execute("getTarget")
    entity_id_str = result.get_value("EntityID") or "-1"
    if entity_id_str == "-1":
      return None
    return EntityID(int(entity_id_str))
