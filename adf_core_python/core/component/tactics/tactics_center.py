from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, List, Optional

if TYPE_CHECKING:
    from adf_core_python.core.agent.communication.message_manager import MessageManager
    from adf_core_python.core.agent.develop.develop_data import DevelopData
    from adf_core_python.core.agent.info.agent_info import AgentInfo
    from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
    from adf_core_python.core.agent.info.world_info import WorldInfo
    from adf_core_python.core.agent.module.module_manager import ModuleManager
    from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData
    from adf_core_python.core.component.module.abstract_module import AbstractModule


class TacticsCenter(ABC):
    def __init__(self, parent: Optional[TacticsCenter] = None) -> None:
        self._parent = parent
        self._modules: List[AbstractModule] = []
        self._command_pickers: List[Any] = []

    @abstractmethod
    def initialize(
        self,
        agent_info: AgentInfo,
        world_info: WorldInfo,
        scenario_info: ScenarioInfo,
        module_manager: ModuleManager,
        precompute_data: PrecomputeData,
        message_manager: MessageManager,
        develop_data: DevelopData,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def resume(
        self,
        agent_info: AgentInfo,
        world_info: WorldInfo,
        scenario_info: ScenarioInfo,
        module_manager: ModuleManager,
        precompute_data: PrecomputeData,
        message_manager: MessageManager,
        develop_data: DevelopData,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def prepare(
        self,
        agent_info: AgentInfo,
        world_info: WorldInfo,
        scenario_info: ScenarioInfo,
        module_manager: ModuleManager,
        precompute_data: PrecomputeData,
        develop_data: DevelopData,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def think(
        self,
        agent_info: AgentInfo,
        world_info: WorldInfo,
        scenario_info: ScenarioInfo,
        module_manager: ModuleManager,
        precompute_data: PrecomputeData,
        message_manager: MessageManager,
        develop_data: DevelopData,
    ) -> None:
        raise NotImplementedError

    def get_parent_tactics(self) -> Optional[TacticsCenter]:
        return self._parent

    def register_module(self, module: AbstractModule) -> None:
        self._modules.append(module)

    def unregister_module(self, module: AbstractModule) -> None:
        self._modules.remove(module)

    def register_command_picker(self, command_picker: Any) -> None:
        self._command_pickers.append(command_picker)

    def unregister_command_picker(self, command_picker: Any) -> None:
        self._command_pickers.remove(command_picker)

    def module_precompute(self, precompute_data: PrecomputeData) -> None:
        for module in self._modules:
            module.precompute(precompute_data)
        for command_picker in self._command_pickers:
            command_picker.precompute(precompute_data)

    def module_resume(self, precompute_data: PrecomputeData) -> None:
        for module in self._modules:
            module.resume(precompute_data)
        for command_picker in self._command_pickers:
            command_picker.resume(precompute_data)

    def module_prepare(self) -> None:
        for module in self._modules:
            module.prepare()
        for command_picker in self._command_pickers:
            command_picker.prepare()

    def module_update_info(self, message_manager: MessageManager) -> None:
        for module in self._modules:
            module.update_info(message_manager)
        for command_picker in self._command_pickers:
            command_picker.update_info(message_manager)
