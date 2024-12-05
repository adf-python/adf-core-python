from typing import Optional

from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.communication.message_manager import MessageManager
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.info.agent_info import AgentInfo
from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
from adf_core_python.core.agent.info.world_info import WorldInfo
from adf_core_python.core.agent.module.module_manager import ModuleManager
from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData
from adf_core_python.core.component.module.complex.human_detector import HumanDetector
from adf_core_python.core.component.module.complex.target_detector import (
    TargetDetector,
    T,
)


class JavaHumanDetector(HumanDetector):
    def __init__(
        self,
        agent_info: AgentInfo,
        world_info: WorldInfo,
        scenario_info: ScenarioInfo,
        module_manager: ModuleManager,
        develop_data: DevelopData,
    ) -> None:
        super().__init__(
            agent_info, world_info, scenario_info, module_manager, develop_data
        )

    def precompute(self, precompute_data: PrecomputeData) -> HumanDetector:
        super().precompute(precompute_data)
        return self

    def resume(self, precompute_data: PrecomputeData) -> HumanDetector:
        super().resume(precompute_data)
        return self

    def prepare(self) -> HumanDetector:
        super().prepare()
        return self

    def calculate(self) -> HumanDetector:
        pass

    def get_target_entity_id(self) -> Optional[EntityID]:
        pass

    def update_info(self, message_manager: MessageManager) -> TargetDetector[T]:
        return super().update_info(message_manager)
