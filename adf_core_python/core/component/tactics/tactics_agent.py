from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from adf_core_python.core.agent.action.action import Action
    from adf_core_python.core.agent.communication.message_manager import MessageManager
    from adf_core_python.core.agent.develop.develop_data import DevelopData
    from adf_core_python.core.agent.info.agent_info import AgentInfo
    from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
    from adf_core_python.core.agent.info.world_info import WorldInfo
    from adf_core_python.core.agent.module.module_manager import ModuleManager
    from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData
    from adf_core_python.core.component.extaction.ext_action import ExtAction
    from adf_core_python.core.component.module.abstract_module import AbstractModule


class TacticsAgent(ABC):
    def __init__(self, parent: Optional[TacticsAgent] = None) -> None:
        self._parent = parent
        self._modules: list[AbstractModule] = []
        self._actions: list[ExtAction] = []
        self._command_executor: Any = None

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
    def precompute(
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
    ) -> Action:
        raise NotImplementedError

    def get_parent_tactics(self) -> Optional[TacticsAgent]:
        return self._parent

    def register_module(self, module: AbstractModule) -> None:
        self._modules.append(module)

    def unregister_module(self, module: AbstractModule) -> None:
        self._modules.remove(module)

    def register_action(self, action: ExtAction) -> None:
        self._actions.append(action)

    def unregister_action(self, action: ExtAction) -> None:
        self._actions.remove(action)

    def register_command_executor(self, command_executor: Any) -> None:
        self._command_executor = command_executor

    def unregister_command_executor(self) -> None:
        self._command_executor = None

    def module_precompute(self, precompute_data: PrecomputeData) -> None:
        for module in self._modules:
            module.precompute(precompute_data)
        for action in self._actions:
            action.precompute(precompute_data)
        for executor in self._command_executor:
            executor.precompute(precompute_data)

    def module_resume(self, precompute_data: PrecomputeData) -> None:
        for module in self._modules:
            module.resume(precompute_data)
        for action in self._actions:
            action.resume(precompute_data)
        for executor in self._command_executor:
            executor.resume(precompute_data)

    def module_prepare(self) -> None:
        for module in self._modules:
            module.prepare()
        for action in self._actions:
            action.prepare()
        for executor in self._command_executor:
            executor.prepare()

    def module_update_info(self, message_manager: MessageManager) -> None:
        for module in self._modules:
            module.update_info(message_manager)
        for action in self._actions:
            action.update_info(message_manager)
        for executor in self._command_executor:
            executor.update_info(message_manager)
