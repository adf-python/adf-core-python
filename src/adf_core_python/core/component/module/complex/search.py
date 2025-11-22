from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from rcrscore.entities.area import Area

from adf_core_python.core.component.module.complex import (
  TargetDetector,
)

if TYPE_CHECKING:
  from adf_core_python.core.agent.develop import DevelopData
  from adf_core_python.core.agent.info import AgentInfo, ScenarioInfo, WorldInfo
  from adf_core_python.core.agent.module import ModuleManager
  from adf_core_python.core.agent.precompute import PrecomputeData


class Search(TargetDetector[Area]):
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

  def precompute(self, precompute_data: PrecomputeData) -> Search:
    super().precompute(precompute_data)
    return self

  def resume(self, precompute_data: PrecomputeData) -> Search:
    super().resume(precompute_data)
    return self

  def prepare(self) -> Search:
    super().prepare()
    return self

  @abstractmethod
  def calculate(self) -> Search:
    return self
