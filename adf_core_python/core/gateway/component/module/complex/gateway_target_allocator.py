from __future__ import annotations

from typing import TYPE_CHECKING

from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.component.module.complex.target_allocator import (
    TargetAllocator,
)
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


class GatewayTargetAllocator(GatewayAbstractModule, TargetAllocator):
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

    def precompute(self, precompute_data: PrecomputeData) -> GatewayTargetAllocator:
        super().precompute(precompute_data)
        return self

    def resume(self, precompute_data: PrecomputeData) -> GatewayTargetAllocator:
        super().resume(precompute_data)
        return self

    def prepare(self) -> GatewayTargetAllocator:
        super().prepare()
        return self

    def update_info(self, message_manager: MessageManager) -> GatewayTargetAllocator:
        super().update_info(message_manager)
        return self

    def calculate(self) -> GatewayTargetAllocator:
        super().calculate()
        return self

    def get_result(self) -> dict[EntityID, EntityID]:
        response = self._gateway_module.execute("getResult")
        response_keys = response.get_all_keys()
        result: dict[EntityID, EntityID] = {}
        for key in response_keys:
            result[EntityID(int(key))] = EntityID(
                int(response.get_value_or_default(key, "-1"))
            )

        return result
