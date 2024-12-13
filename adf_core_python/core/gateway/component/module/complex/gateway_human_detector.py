from __future__ import annotations

from typing import TYPE_CHECKING

from rcrs_core.entities.human import Human

from adf_core_python.core.component.module.complex.human_detector import (
    HumanDetector,
)
from adf_core_python.core.gateway.component.module.complex.gateway_target_detector import (
    GatewayTargetDetector,
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


class GatewayHumanDetector(GatewayTargetDetector[Human], HumanDetector):
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

    def precompute(self, precompute_data: PrecomputeData) -> GatewayHumanDetector:
        super().precompute(precompute_data)
        return self

    def resume(self, precompute_data: PrecomputeData) -> GatewayHumanDetector:
        super().resume(precompute_data)
        return self

    def prepare(self) -> GatewayHumanDetector:
        super().prepare()
        return self

    def update_info(self, message_manager: MessageManager) -> GatewayHumanDetector:
        super().update_info(message_manager)
        return self

    def calculate(self) -> GatewayHumanDetector:
        super().calculate()
        return self
