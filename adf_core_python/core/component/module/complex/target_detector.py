from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Generic, Optional, TypeVar

from rcrscore.entities.entity import Entity

from adf_core_python.core.component.module.abstract_module import AbstractModule

if TYPE_CHECKING:
    from rcrscore.entities import EntityID

    from adf_core_python.core.agent.communication.message_manager import MessageManager
    from adf_core_python.core.agent.develop.develop_data import DevelopData
    from adf_core_python.core.agent.info.agent_info import AgentInfo
    from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
    from adf_core_python.core.agent.info.world_info import WorldInfo
    from adf_core_python.core.agent.module.module_manager import ModuleManager
    from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData

T = TypeVar("T", bound=Entity)


class TargetDetector(AbstractModule, Generic[T]):
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
    def get_target_entity_id(self) -> Optional[EntityID]:
        pass

    @abstractmethod
    def calculate(self) -> TargetDetector[T]:
        pass

    def precompute(self, precompute_data: PrecomputeData) -> TargetDetector[T]:
        super().precompute(precompute_data)
        return self

    def resume(self, precompute_data: PrecomputeData) -> TargetDetector[T]:
        super().resume(precompute_data)
        return self

    def prepare(self) -> TargetDetector[T]:
        super().prepare()
        return self

    def update_info(self, message_manager: MessageManager) -> TargetDetector[T]:
        super().update_info(message_manager)
        return self
