from __future__ import annotations

from typing import TYPE_CHECKING

from adf_core_python.core.component.module import AbstractModule

if TYPE_CHECKING:
  from adf_core_python.core.agent.communication import MessageManager
  from adf_core_python.core.agent.develop import DevelopData
  from adf_core_python.core.agent.info import AgentInfo, ScenarioInfo, WorldInfo
  from adf_core_python.core.agent.module import ModuleManager
  from adf_core_python.core.agent.precompute import PrecomputeData
  from adf_core_python.core.gateway import GatewayModule


class GatewayAbstractModule(AbstractModule):
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
      agent_info, world_info, scenario_info, module_manager, develop_data
    )
    self._gateway_module = gateway_module

  def precompute(self, precompute_data: PrecomputeData) -> GatewayAbstractModule:
    super().precompute(precompute_data)
    self._gateway_module.execute("precompute")
    return self

  def resume(self, precompute_data: PrecomputeData) -> GatewayAbstractModule:
    super().resume(precompute_data)
    self._gateway_module.execute("resume")
    return self

  def prepare(self) -> GatewayAbstractModule:
    super().prepare()
    self._gateway_module.execute("preparate")
    return self

  def update_info(self, message_manager: MessageManager) -> GatewayAbstractModule:
    super().update_info(message_manager)
    self._gateway_module.execute("updateInfo")
    return self

  def calculate(self) -> GatewayAbstractModule:
    self._gateway_module.execute("calc")
    return self
