from typing import Optional, cast

from rcrscore.entities import Area, Blockade, EntityID, FireBrigade, Human

from adf_core_python.core.agent.action import Action
from adf_core_python.core.agent.action.ambulance import ActionRescue
from adf_core_python.core.agent.action.common import ActionMove
from adf_core_python.core.agent.communication import MessageManager
from adf_core_python.core.agent.develop import DevelopData
from adf_core_python.core.agent.info import (
  AgentInfo,
  ScenarioInfo,
  ScenarioInfoKeys,
  WorldInfo,
)
from adf_core_python.core.agent.module import ModuleManager
from adf_core_python.core.agent.precompute import PrecomputeData
from adf_core_python.core.component.action import ExtendAction
from adf_core_python.core.component.module.algorithm import PathPlanning


class DefaultExtendActionRescue(ExtendAction):
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
    self._kernel_time: int = -1
    self._target_entity_id: Optional[EntityID] = None
    self._threshold_rest = develop_data.get_value(
      "adf_core_python.implement.action.DefaultExtendActionRescue.rest", 100
    )

    self._path_planning = cast(
      "PathPlanning",
      self.module_manager.get_module(
        "DefaultExtendActionRescue.PathPlanning",
        "adf_core_python.implement.module.algorithm.a_star_path_planning.AStarPathPlanning",
      ),
    )

  def precompute(self, precompute_data: PrecomputeData) -> ExtendAction:
    super().precompute(precompute_data)
    if self.get_count_precompute() >= 2:
      return self
    self._path_planning.precompute(precompute_data)
    self._kernel_time = self.scenario_info.get_value(
      ScenarioInfoKeys.KERNEL_TIMESTEPS, -1
    )
    return self

  def resume(self, precompute_data: PrecomputeData) -> ExtendAction:
    super().resume(precompute_data)
    if self.get_count_resume() >= 2:
      return self
    self._path_planning.resume(precompute_data)
    self._kernel_time = self.scenario_info.get_value(
      ScenarioInfoKeys.KERNEL_TIMESTEPS, -1
    )
    return self

  def prepare(self) -> ExtendAction:
    super().prepare()
    if self.get_count_prepare() >= 2:
      return self
    self._path_planning.prepare()
    self._kernel_time = self.scenario_info.get_value(
      ScenarioInfoKeys.KERNEL_TIMESTEPS, -1
    )
    return self

  def update_info(self, message_manager: MessageManager) -> ExtendAction:
    super().update_info(message_manager)
    if self.get_count_update_info() >= 2:
      return self
    self._path_planning.update_info(message_manager)
    return self

  def set_target_entity_id(self, target_entity_id: EntityID) -> ExtendAction:
    self._target_entity_id = None
    if target_entity_id is not None:
      entity = self.world_info.get_entity(target_entity_id)
      if isinstance(entity, Human) or isinstance(entity, Area):
        self._target_entity_id = target_entity_id
        return self
    return self

  def calculate(self) -> ExtendAction:
    self.result = None
    agent = cast("FireBrigade", self.agent_info.get_myself())

    if self._target_entity_id is not None:
      self.result = self._calc_rescue(
        agent, self._path_planning, self._target_entity_id
      )

    return self

  def _calc_rescue(
    self,
    agent: FireBrigade,
    path_planning: PathPlanning,
    target_entity_id: EntityID,
  ) -> Optional[Action]:
    target_entity = self.world_info.get_entity(target_entity_id)
    if target_entity is None:
      return None

    agent_position_entity_id = agent.get_position()
    if agent_position_entity_id is None:
      return None

    if isinstance(target_entity, Human):
      human = target_entity
      if human.get_hp() == 0:
        return None

      target_position_entity_id = human.get_position()
      if target_position_entity_id is None:
        return None

      if agent_position_entity_id == target_position_entity_id:
        buriedness = human.get_buriedness()
        if buriedness is not None and buriedness > 0:
          return ActionRescue(target_entity_id)
      else:
        path = path_planning.get_path(
          agent_position_entity_id, target_position_entity_id
        )
        if path != []:
          return ActionMove(path)

      return None

    if isinstance(target_entity, Blockade):
      blockade = target_entity
      blockade_position = blockade.get_position()
      if blockade_position is None:
        return None

      target_entity = self.world_info.get_entity(blockade_position)
      if isinstance(target_entity, Area):
        path = self._path_planning.get_path(
          agent_position_entity_id, target_entity.get_entity_id()
        )
        if path != []:
          return ActionMove(path)

    return None
