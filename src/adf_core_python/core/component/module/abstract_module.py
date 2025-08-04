from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from adf_core_python.core.logger.logger import get_agent_logger

if TYPE_CHECKING:
  from adf_core_python.core.agent.communication.message_manager import MessageManager
  from adf_core_python.core.agent.develop.develop_data import DevelopData
  from adf_core_python.core.agent.info.agent_info import AgentInfo
  from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
  from adf_core_python.core.agent.info.world_info import WorldInfo
  from adf_core_python.core.agent.module.module_manager import ModuleManager
  from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData


class AbstractModule(ABC):
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
    self._count_resume: int = 0
    self._count_prepare: int = 0
    self._count_update_info: int = 0
    self._count_update_info_current_time: int = 0
    self._logger = get_agent_logger(
      f"{self.__class__.__module__}.{self.__class__.__qualname__}",
      self._agent_info,
    )

    self._sub_modules: list[AbstractModule] = []

  def register_sub_module(self, sub_module: AbstractModule) -> None:
    self._sub_modules.append(sub_module)

  def unregister_sub_module(self, sub_module: AbstractModule) -> None:
    self._sub_modules.remove(sub_module)

  def precompute(self, precompute_data: PrecomputeData) -> AbstractModule:
    self._count_precompute += 1
    for sub_module in self._sub_modules:
      sub_module.precompute(precompute_data)
    return self

  def resume(self, precompute_data: PrecomputeData) -> AbstractModule:
    self._count_resume += 1
    for sub_module in self._sub_modules:
      sub_module.resume(precompute_data)
    return self

  def prepare(self) -> AbstractModule:
    self._count_prepare += 1
    for sub_module in self._sub_modules:
      start_time = time.time()
      sub_module.prepare()
      self._logger.debug(
        f"{self.__class__.__name__}'s sub_module {sub_module.__class__.__name__} prepare time: {time.time() - start_time:.3f}",
      )
    return self

  def update_info(self, message_manager: MessageManager) -> AbstractModule:
    self._count_update_info += 1
    for sub_module in self._sub_modules:
      sub_module.update_info(message_manager)
    return self

  @abstractmethod
  def calculate(self) -> AbstractModule:
    raise NotImplementedError

  def get_count_precompute(self) -> int:
    return self._count_precompute

  def get_count_resume(self) -> int:
    return self._count_resume

  def get_count_prepare(self) -> int:
    return self._count_prepare

  def get_count_update_info(self) -> int:
    return self._count_update_info

  def reset_count_precompute(self) -> None:
    self._count_precompute = 0

  def reset_count_resume(self) -> None:
    self._count_resume = 0

  def reset_count_prepare(self) -> None:
    self._count_prepare = 0

  def reset_count_update_info(self) -> None:
    self._count_update_info = 0
