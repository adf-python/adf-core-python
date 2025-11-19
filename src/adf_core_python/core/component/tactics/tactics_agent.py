from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

from adf_core_python.core.logger.logger import get_agent_logger

if TYPE_CHECKING:
  from adf_core_python.core.component.centralized.command_executor import CommandExecutor
  from adf_core_python.core.agent.action.action import Action
  from adf_core_python.core.agent.communication.message_manager import MessageManager
  from adf_core_python.core.agent.develop.develop_data import DevelopData
  from adf_core_python.core.agent.info.agent_info import AgentInfo
  from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
  from adf_core_python.core.agent.info.world_info import WorldInfo
  from adf_core_python.core.agent.module.module_manager import ModuleManager
  from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData
  from adf_core_python.core.component.action.extend_action import ExtendAction
  from adf_core_python.core.component.module.abstract_module import AbstractModule


class TacticsAgent(ABC):
  def __init__(self, parent: Optional[TacticsAgent] = None) -> None:
    self._parent = parent
    self._modules: list[AbstractModule] = []
    self._actions: list[ExtendAction] = []
    self._command_executor: list[CommandExecutor] = []

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
    self._logger = get_agent_logger(
      f"{self.__class__.__module__}.{self.__class__.__qualname__}", agent_info
    )

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

  def register_action(self, action: ExtendAction) -> None:
    self._actions.append(action)

  def unregister_action(self, action: ExtendAction) -> None:
    self._actions.remove(action)

  def register_command_executor(self, command_executor: CommandExecutor) -> None:
    self._command_executor.append(command_executor)

  def unregister_command_executor(self, command_executor: CommandExecutor) -> None:
    self._command_executor.remove(command_executor)

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
      start_time = time.time()
      module.prepare()
      self._logger.debug(
        f"module {module.__class__.__name__} prepare time: {time.time() - start_time:.3f}",
      )
    for action in self._actions:
      start_time = time.time()
      action.prepare()
      self._logger.debug(
        f"module {action.__class__.__name__} prepare time: {time.time() - start_time:.3f}",
      )
    for executor in self._command_executor:
      executor.prepare()

  def module_update_info(self, message_manager: MessageManager) -> None:
    for module in self._modules:
      module.update_info(message_manager)
    for action in self._actions:
      action.update_info(message_manager)
    for executor in self._command_executor:
      executor.update_info(message_manager)

  def reset_count(self) -> None:
    for module in self._modules:
      module.reset_count_precompute()
      module.reset_count_resume()
      module.reset_count_prepare()
      module.reset_count_update_info()
    for action in self._actions:
      action.reset_count_precompute()
      action.reset_count_resume()
      action.reset_count_prepare()
      action.reset_count_update_info()
    for executor in self._command_executor:
      executor.reset_count_precompute()
      executor.reset_count_resume()
      executor.reset_count_prepare()
      executor.reset_count_update_info()
