from typing import TYPE_CHECKING, Optional, cast

from rcrscore.entities import Area, Blockade, Entity, EntityID, Human

from adf_core_python.core.agent.action.common import ActionMove
from adf_core_python.core.agent.communication import MessageManager
from adf_core_python.core.agent.develop import DevelopData
from adf_core_python.core.agent.info import AgentInfo, ScenarioInfo, WorldInfo
from adf_core_python.core.agent.module import ModuleManager
from adf_core_python.core.agent.precompute import PrecomputeData
from adf_core_python.core.component.action import ExtendAction

if TYPE_CHECKING:
  from adf_core_python.core.component.module.algorithm.path_planning import PathPlanning


class DefaultExtendActionMove(ExtendAction):
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
    self._target_entity_id: Optional[EntityID] = None
    self._threshold_to_rest: int = develop_data.get_value("threshold_to_rest", 100)

    self._path_planning: PathPlanning = cast(
      "PathPlanning",
      self.module_manager.get_module(
        "DefaultExtendActionMove.PathPlanning",
        "adf_core_python.implement.module.algorithm.a_star_path_planning.AStarPathPlanning",
      ),
    )

  def precompute(self, precompute_data: PrecomputeData) -> ExtendAction:
    super().precompute(precompute_data)
    if self.get_count_precompute() > 1:
      return self
    self._path_planning.precompute(precompute_data)
    return self

  def resume(self, precompute_data: PrecomputeData) -> ExtendAction:
    super().resume(precompute_data)
    if self.get_count_resume() > 1:
      return self
    self._path_planning.resume(precompute_data)
    return self

  def prepare(self) -> ExtendAction:
    super().prepare()
    if self.get_count_prepare() > 1:
      return self
    self._path_planning.prepare()
    return self

  def update_info(self, message_manager: MessageManager) -> ExtendAction:
    super().update_info(message_manager)
    if self.get_count_update_info() > 1:
      return self
    self._path_planning.update_info(message_manager)
    return self

  def set_target_entity_id(self, target_entity_id: EntityID) -> ExtendAction:
    entity: Optional[Entity] = self.world_info.get_entity(target_entity_id)
    self._target_entity_id = None

    if entity is None:
      return self

    if isinstance(entity, Blockade) or isinstance(entity, Human):
      position: Optional[EntityID] = entity.get_position()
      if position is None:
        return self
      entity = self.world_info.get_entity(position)

    if entity is not None and isinstance(entity, Area):
      self._target_entity_id = entity.get_entity_id()

    return self

  def calculate(self) -> ExtendAction:
    self.result = None
    agent: Human = cast("Human", self.agent_info.get_myself())

    if self._target_entity_id is None:
      return self

    agent_position = agent.get_position()
    if agent_position is None:
      return self

    path: list[EntityID] = self._path_planning.get_path(
      agent_position, self._target_entity_id
    )

    if path is not None and len(path) != 0:
      self.result = ActionMove(path)

    return self
