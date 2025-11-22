from typing import TYPE_CHECKING, Optional, cast

from adf_core_python.core.agent.action import Action
from adf_core_python.core.agent.action.common import ActionRest
from adf_core_python.core.agent.communication import MessageManager
from adf_core_python.core.agent.communication.standard.bundle.centralized import (
  CommandFire,
  CommandScout,
)
from adf_core_python.core.agent.develop import DevelopData
from adf_core_python.core.agent.info import AgentInfo, ScenarioInfo, WorldInfo
from adf_core_python.core.agent.module import ModuleManager
from adf_core_python.core.agent.precompute import PrecomputeData
from adf_core_python.core.component.tactics import (
  TacticsFireBrigade,
)

if TYPE_CHECKING:
  from rcrscore.entities import FireBrigade

  from adf_core_python.core.agent.communication.standard.bundle import (
    StandardMessage,
  )
  from adf_core_python.core.component.module.complex import HumanDetector, Search


class DefaultTacticsFireBrigade(TacticsFireBrigade):
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
    # world_info.index_class()
    super().initialize(
      agent_info,
      world_info,
      scenario_info,
      module_manager,
      precompute_data,
      message_manager,
      develop_data,
    )

    self._search: Search = cast(
      "Search",
      module_manager.get_module(
        "DefaultTacticsFireBrigade.Search",
        "adf_core_python.implement.module.complex.default_search.DefaultSearch",
      ),
    )
    self._human_detector: HumanDetector = cast(
      "HumanDetector",
      module_manager.get_module(
        "DefaultTacticsFireBrigade.HumanDetector",
        "adf_core_python.implement.module.complex.default_human_detector.DefaultHumanDetector",
      ),
    )
    self._action_rescue = module_manager.get_extend_action(
      "DefaultTacticsFireBrigade.ExtendActionRescue",
      "adf_core_python.implement.action.default_extend_action_rescue.DefaultExtendActionRescue",
    )
    self._action_ext_move = module_manager.get_extend_action(
      "DefaultTacticsAmbulanceTeam.ExtendActionMove",
      "adf_core_python.implement.action.default_extend_action_move.DefaultExtendActionMove",
    )
    self._command_executor_fire = module_manager.get_command_executor(
      "DefaultTacticsFireBrigade.CommandExecutorFire",
      "adf_core_python.implement.centralized.default_command_executor_fire.DefaultCommandExecutorFire",
    )
    self._command_executor_scout = module_manager.get_command_executor(
      "DefaultTacticsAmbulanceTeam.CommandExecutorScout",
      "adf_core_python.implement.centralized.default_command_executor_scout.DefaultCommandExecutorScout",
    )

    self.register_module(self._search)
    self.register_module(self._human_detector)
    self.register_action(self._action_rescue)
    self.register_action(self._action_ext_move)
    self.register_command_executor(self._command_executor_fire)
    self.register_command_executor(self._command_executor_scout)

    self._recent_command: Optional[StandardMessage] = None

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
    self.module_precompute(precompute_data)

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
    self.module_resume(precompute_data)

  def prepare(
    self,
    agent_info: AgentInfo,
    world_info: WorldInfo,
    scenario_info: ScenarioInfo,
    module_manager: ModuleManager,
    precompute_data: PrecomputeData,
    develop_data: DevelopData,
  ) -> None:
    self.module_prepare()

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
    self.reset_count()
    self.module_update_info(message_manager)

    agent: FireBrigade = cast("FireBrigade", agent_info.get_myself())  # noqa: F841
    entity_id = agent_info.get_entity_id()  # noqa: F841

    for message in message_manager.get_received_message_list():
      if isinstance(message, CommandScout):
        if message.get_command_executor_agent_entity_id() == agent_info.get_entity_id():
          self._recent_command = message
          self._command_executor_scout.set_command(command=message)
      if isinstance(message, CommandFire):
        if message.get_command_executor_agent_entity_id() == agent_info.get_entity_id():
          self._recent_command = message
          self._command_executor_fire.set_command(message)

    if self._recent_command is not None:
      action: Optional[Action] = None
      if isinstance(self._recent_command, CommandScout):
        action = self._command_executor_scout.calculate().get_action()
      elif isinstance(self._recent_command, CommandFire):
        action = self._command_executor_fire.calculate().get_action()
      if action is not None:
        self._logger.debug(
          f"action decided by command: {action}", time=agent_info.get_time()
        )
        return action

    target_entity_id = self._human_detector.calculate().get_target_entity_id()
    self._logger.debug(
      f"human detector target_entity_id: {target_entity_id}",
      time=agent_info.get_time(),
    )
    if target_entity_id is not None:
      action = (
        self._action_rescue.set_target_entity_id(target_entity_id)
        .calculate()
        .get_action()
      )
      if action is not None:
        self._logger.debug(f"action: {action}", time=agent_info.get_time())
        return action

    target_entity_id = self._search.calculate().get_target_entity_id()
    self._logger.debug(
      f"search target_entity_id: {target_entity_id}", time=agent_info.get_time()
    )
    if target_entity_id is not None:
      action = (
        self._action_ext_move.set_target_entity_id(target_entity_id)
        .calculate()
        .get_action()
      )
      if action is not None:
        self._logger.debug(f"action: {action}", time=agent_info.get_time())
        return action

    return ActionRest()
