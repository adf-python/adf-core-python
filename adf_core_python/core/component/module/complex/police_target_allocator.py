from abc import abstractmethod
from rcrs_core.worldmodel.entityID import EntityID
from adf_core_python.core.agent.communication.message_manager import MessageManager
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.info.agent_info import AgentInfo
from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
from adf_core_python.core.agent.info.world_info import WorldInfo
from adf_core_python.core.agent.module.module_manager import ModuleManager
from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData
from adf_core_python.core.component.module.complex.target_allocator import (
    TargetAllocator,
)


class PoliceTargetAllocator(TargetAllocator):
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

    @abstractmethod
    def get_result(self) -> dict[EntityID, EntityID]:
        pass

    @abstractmethod
    def calculate(self) -> TargetAllocator:
        pass

    def resume(self, precompute_data: PrecomputeData) -> TargetAllocator:
        super().resume(precompute_data)
        return self

    def prepare(self) -> TargetAllocator:
        super().prepare()
        return self

    def update_info(self, message_manager: MessageManager) -> TargetAllocator:
        super().update_info(message_manager)
        return self
