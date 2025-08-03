from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from rcrscore.entities import EntityID

    from adf_core_python.core.agent.action.action import Action
    from adf_core_python.core.agent.communication.message_manager import MessageManager
    from adf_core_python.core.agent.develop.develop_data import DevelopData
    from adf_core_python.core.agent.info.agent_info import AgentInfo
    from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
    from adf_core_python.core.agent.info.world_info import WorldInfo
    from adf_core_python.core.agent.module.module_manager import ModuleManager
    from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData


class ExtendAction(ABC):
    def __init__(
        self,
        agent_info: AgentInfo,
        world_info: WorldInfo,
        scenario_info: ScenarioInfo,
        module_manager: ModuleManager,
        develop_data: DevelopData,
    ):
        self.world_info = world_info
        self.agent_info = agent_info
        self.scenario_info = scenario_info
        self.module_manager = module_manager
        self.develop_data = develop_data
        self.result: Optional[Action] = None
        self.count_precompute: int = 0
        self.count_resume: int = 0
        self.count_prepare: int = 0
        self.count_update_info: int = 0
        self.count_update_info_current_time: int = 0

    @abstractmethod
    def set_target_entity_id(self, target_entity_id: EntityID) -> ExtendAction:
        raise NotImplementedError

    @abstractmethod
    def calculate(self) -> ExtendAction:
        raise NotImplementedError

    def get_action(self) -> Optional[Action]:
        return self.result

    def precompute(self, precompute_data: PrecomputeData) -> ExtendAction:
        self.count_precompute += 1
        return self

    def resume(self, precompute_data: PrecomputeData) -> ExtendAction:
        self.count_resume += 1
        return self

    def prepare(self) -> ExtendAction:
        self.count_prepare += 1
        return self

    def update_info(self, message_manager: MessageManager) -> ExtendAction:
        self.count_update_info += 1
        return self

    def get_count_precompute(self) -> int:
        return self.count_precompute

    def get_count_resume(self) -> int:
        return self.count_resume

    def get_count_prepare(self) -> int:
        return self.count_prepare

    def get_count_update_info(self) -> int:
        return self.count_update_info

    def reset_count_precompute(self) -> None:
        self.count_precompute = 0

    def reset_count_resume(self) -> None:
        self.count_resume = 0

    def reset_count_prepare(self) -> None:
        self.count_prepare = 0

    def reset_count_update_info(self) -> None:
        self.count_update_info = 0
