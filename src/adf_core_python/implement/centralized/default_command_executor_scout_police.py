from typing import TYPE_CHECKING, Optional, cast

from rcrscore.entities import Building, EntityID, Human, Refuge, Road

from adf_core_python.core.agent.action.common import ActionMove
from adf_core_python.core.agent.communication import MessageManager
from adf_core_python.core.agent.communication.standard.bundle import (
  StandardMessagePriority,
)
from adf_core_python.core.agent.communication.standard.bundle.centralized import (
  CommandScout,
  MessageReport,
)
from adf_core_python.core.agent.develop import DevelopData
from adf_core_python.core.agent.info import AgentInfo, ScenarioInfo, WorldInfo
from adf_core_python.core.agent.module import ModuleManager
from adf_core_python.core.agent.precompute import PrecomputeData
from adf_core_python.core.component.centralized import CommandExecutor

if TYPE_CHECKING:
  from adf_core_python.core.component.action import ExtendAction
  from adf_core_python.core.component.module.algorithm import PathPlanning


class DefaultCommandExecutorScoutPolice(CommandExecutor):
  ACTION_UNKNOWN: int = -1
  ACTION_SCOUT: int = 1

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

    self._path_planning: PathPlanning = cast(
      "PathPlanning",
      module_manager.get_module(
        "DefaultCommandExecutorScoutPolice.PathPlanning",
        "adf_core_python.implement.module.algorithm.a_star_path_planning.AStarPathPlanning",
      ),
    )
    self._action_clear: ExtendAction = module_manager.get_extend_action(
      "DefaultCommandExecutorScoutPolice.ExtendActionClear",
      "adf_core_python.implement.action.default_extend_action_clear.DefaultExtendActionClear",
    )

    self._command_type: int = self.ACTION_UNKNOWN
    self._targets: list[EntityID] = []
    self._commander: Optional[EntityID] = None

  def set_command(self, command: CommandScout) -> CommandExecutor:
    agent_id: EntityID = self._agent_info.get_entity_id()
    if command.get_command_executor_agent_entity_id() != agent_id:
      return self

    target = command.get_command_target_entity_id()
    if target is None:
      target = self._agent_info.get_position_entity_id()
      if target is None:
        return self

    self._command_type = self.ACTION_SCOUT
    self._commander = command.get_sender_entity_id()
    self._targets = []
    if (scout_distance := command.get_scout_range()) is None:
      return self

    for entity in self._world_info.get_entities_of_types([Road, Building, Refuge]):
      if isinstance(entity, Refuge):
        continue
      if (
        self._world_info.get_distance(target, entity.get_entity_id()) <= scout_distance
      ):
        self._targets.append(entity.get_entity_id())

    return self

  def calculate(self) -> CommandExecutor:
    self._result = None
    match self._command_type:
      case self.ACTION_SCOUT:
        if len(self._targets) == 0:
          return self
        agent_position = self._agent_info.get_position_entity_id()
        if agent_position is None:
          return self
        path = self._path_planning.get_path(agent_position, self._targets[0])
        if path is None:
          return self
        action = (
          self._action_clear.set_target_entity_id(self._targets[0])
          .calculate()
          .get_action()
        )
        if action is None:
          action = ActionMove(path)
        self._result = action
      case _:
        return self
    return self

  def update_info(self, message_manager: MessageManager) -> CommandExecutor:
    super().update_info(message_manager)
    if self.get_count_update_info() >= 2:
      return self

    self._path_planning.update_info(message_manager)

    if self._is_command_completed():
      if self._command_type == self.ACTION_UNKNOWN:
        return self
      if self._commander is None:
        return self

      message_manager.add_message(
        MessageReport(
          True,
          True,
          False,
          self._commander,
          StandardMessagePriority.NORMAL,
        )
      )
      self._command_type = self.ACTION_UNKNOWN
      self._target = None
      self._commander = None

    return self

  def precompute(self, precompute_data: PrecomputeData) -> CommandExecutor:
    super().precompute(precompute_data)
    if self.get_count_precompute() >= 2:
      return self
    self._path_planning.precompute(precompute_data)
    return self

  def resume(self, precompute_data: PrecomputeData) -> CommandExecutor:
    super().resume(precompute_data)
    if self.get_count_resume() >= 2:
      return self
    self._path_planning.resume(precompute_data)
    return self

  def prepare(self) -> CommandExecutor:
    super().prepare()
    if self.get_count_prepare() >= 2:
      return self
    self._path_planning.prepare()
    return self

  def _is_command_completed(self) -> bool:
    agent = self._agent_info.get_myself()
    if not isinstance(agent, Human):
      return False

    match self._command_type:
      case self.ACTION_SCOUT:
        if len(self._targets) != 0:
          for entity in self._world_info.get_entities_of_types(
            [Road, Building, Refuge]
          ):
            self._targets.remove(entity.get_entity_id())
        return len(self._targets) == 0
      case _:
        return True
