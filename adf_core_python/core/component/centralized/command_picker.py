from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from rcrscore.entities import EntityID

if TYPE_CHECKING:
    from adf_core_python.core.agent.develop.develop_data import DevelopData
    from adf_core_python.core.agent.info.agent_info import AgentInfo
    from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
    from adf_core_python.core.agent.info.world_info import WorldInfo
    from adf_core_python.core.agent.module.module_manager import ModuleManager

from adf_core_python.core.agent.communication.message_manager import MessageManager
from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData
from adf_core_python.core.component.communication.communication_message import (
    CommunicationMessage,
)


class CommandPicker(ABC):
    def __init__(
        self,
        agent_info: AgentInfo,
        world_info: WorldInfo,
        scenario_info: ScenarioInfo,
        module_manager: ModuleManager,
        develop_data: DevelopData,
    ) -> None:
        self._agent_info = agent_info
        self._world_info = world_info
        self._scenario_info = scenario_info
        self._module_manager = module_manager
        self._develop_data = develop_data
        self._count_precompute: int = 0
        self._count_prepare: int = 0
        self._count_resume: int = 0
        self._count_update_info: int = 0
        self._count_update_info_current_time: int = 0

    @abstractmethod
    def set_allocator_result(
        self, allocation_data: dict[EntityID, EntityID]
    ) -> CommandPicker:
        pass

    @abstractmethod
    def calculate(self) -> CommandPicker:
        pass

    @abstractmethod
    def get_result(self) -> list[CommunicationMessage]:
        pass

    def precompute(self, precompute_data: PrecomputeData) -> CommandPicker:
        self._count_precompute += 1
        return self

    def prepare(self) -> CommandPicker:
        self._count_prepare += 1
        return self

    def resume(self, precompute_data: PrecomputeData) -> CommandPicker:
        self._count_resume += 1
        return self

    def update_info(self, message_manager: MessageManager) -> CommandPicker:
        if self._count_update_info_current_time != self._agent_info.get_time():
            self._count_update_info_current_time = self._agent_info.get_time()
            self._count_update_info = 0
        self._count_update_info += 1
        return self

    def get_count_precompute(self) -> int:
        return self._count_precompute

    def get_count_prepare(self) -> int:
        return self._count_prepare

    def get_count_resume(self) -> int:
        return self._count_resume

    def get_count_update_info(self) -> int:
        return self._count_update_info

    def get_count_update_info_current_time(self) -> int:
        return self._count_update_info_current_time

    def reset_count_precompute(self) -> None:
        self._count_precompute = 0

    def reset_count_prepare(self) -> None:
        self._count_prepare = 0

    def reset_count_resume(self) -> None:
        self._count_resume = 0

    def reset_count_update_info(self) -> None:
        self._count_update_info = 0
