from __future__ import annotations

from typing import TYPE_CHECKING

from adf_core_python.core.component.module.abstract_module import AbstractModule

if TYPE_CHECKING:
    from adf_core_python.core.agent.communication.message_manager import MessageManager
    from adf_core_python.core.agent.develop.develop_data import DevelopData
    from adf_core_python.core.agent.info.agent_info import AgentInfo
    from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
    from adf_core_python.core.agent.info.world_info import WorldInfo
    from adf_core_python.core.agent.module.module_manager import ModuleManager
    from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData
    from adf_core_python.core.gateway.gateway_module import GatewayModule


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
