from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from adf_core_python.core.component.module import AbstractModule

if TYPE_CHECKING:
  from rcrscore.entities import EntityID

  from adf_core_python.core.agent.communication import MessageManager
  from adf_core_python.core.agent.develop import DevelopData
  from adf_core_python.core.agent.info import AgentInfo, ScenarioInfo, WorldInfo
  from adf_core_python.core.agent.module import ModuleManager
  from adf_core_python.core.agent.precompute import PrecomputeData


class PathPlanning(AbstractModule):
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
  def get_path(
    self, from_entity_id: EntityID, to_entity_id: EntityID
  ) -> list[EntityID]:
    pass

  @abstractmethod
  def get_path_to_multiple_destinations(
    self, from_entity_id: EntityID, destination_entity_ids: set[EntityID]
  ) -> list[EntityID]:
    pass

  @abstractmethod
  def get_distance(self, from_entity_id: EntityID, to_entity_id: EntityID) -> float:
    pass

  def precompute(self, precompute_data: PrecomputeData) -> PathPlanning:
    super().precompute(precompute_data)
    return self

  def resume(self, precompute_data: PrecomputeData) -> PathPlanning:
    super().resume(precompute_data)
    return self

  def prepare(self) -> PathPlanning:
    super().prepare()
    return self

  def update_info(self, message_manager: MessageManager) -> PathPlanning:
    super().update_info(message_manager)
    return self

  @abstractmethod
  def calculate(self) -> PathPlanning:
    pass
