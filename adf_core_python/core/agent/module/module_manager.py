from __future__ import annotations

import importlib
from typing import TYPE_CHECKING, Any

from adf_core_python.core.component.action.extend_action import ExtendAction
from adf_core_python.core.component.module.abstract_module import AbstractModule

if TYPE_CHECKING:
    from adf_core_python.core.agent.config.module_config import ModuleConfig
    from adf_core_python.core.agent.develop.develop_data import DevelopData
    from adf_core_python.core.agent.info.agent_info import AgentInfo
    from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
    from adf_core_python.core.agent.info.world_info import WorldInfo


class ModuleManager:
    def __init__(
        self,
        agent_info: AgentInfo,
        world_info: WorldInfo,
        scenario_info: ScenarioInfo,
        module_config: ModuleConfig,
        develop_data: DevelopData,
    ) -> None:
        self._agent_info = agent_info
        self._world_info = world_info
        self._scenario_info = scenario_info
        self._module_config = module_config
        self._develop_data = develop_data
        self._modules: dict[str, AbstractModule] = {}
        self._actions: dict[str, ExtendAction] = {}

        self._executors: dict[str, Any] = {}
        self._pickers: dict[str, Any] = {}
        self._channel_subscribers: dict[str, Any] = {}
        self._message_coordinators: dict[str, Any] = {}

    def get_module(self, module_name: str, default_module_name: str) -> AbstractModule:
        class_name = self._module_config.get_value_or_default(
            module_name, default_module_name
        )

        try:
            module_class: type = self._load_module(class_name)
        except (ImportError, AttributeError) as e:
            raise RuntimeError(f"Failed to load module {class_name}") from e

        instance = self._modules.get(module_name)
        if instance is not None:
            return instance

        if issubclass(module_class, AbstractModule):
            instance = module_class(
                self._agent_info,
                self._world_info,
                self._scenario_info,
                self,
                self._develop_data,
            )
            self._modules[module_name] = instance
            return instance

        raise RuntimeError(f"Module {class_name} is not a subclass of AbstractModule")

    def get_extend_action(
        self, action_name: str, default_action_name: str
    ) -> ExtendAction:
        class_name = self._module_config.get_value_or_default(
            action_name, default_action_name
        )

        try:
            action_class: type = self._load_module(class_name)
        except (ImportError, AttributeError) as e:
            raise RuntimeError(f"Failed to load action {class_name}") from e

        instance = self._actions.get(action_name)
        if instance is not None:
            return instance

        if issubclass(action_class, ExtendAction):
            instance = action_class(
                self._agent_info,
                self._world_info,
                self._scenario_info,
                self,
                self._develop_data,
            )
            self._actions[action_name] = instance
            return instance

        raise RuntimeError(f"Action {class_name} is not a subclass of ExtendAction")

    def _load_module(self, class_name: str) -> type:
        module_name, module_class_name = class_name.rsplit(".", 1)
        module = importlib.import_module(module_name)
        return getattr(module, module_class_name)
