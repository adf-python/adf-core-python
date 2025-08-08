from threading import Event
from typing import Optional

from adf_core_python.core.agent.action.common.action_rest import ActionRest
from adf_core_python.core.agent.agent import Agent
from adf_core_python.core.agent.config.module_config import ModuleConfig
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.info.scenario_info import Mode
from adf_core_python.core.agent.module.module_manager import ModuleManager
from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData
from adf_core_python.core.component.tactics.tactics_center import TacticsCenter
from adf_core_python.core.gateway.gateway_agent import GatewayAgent
from adf_core_python.core.logger.logger import get_agent_logger


class Office(Agent):
  def __init__(
    self,
    tactics_center: TacticsCenter,
    team_name: str,
    is_precompute: bool,
    is_debug: bool,
    data_storage_name: str,
    module_config: ModuleConfig,
    develop_data: DevelopData,
    finish_post_connect_event: Event,
    gateway_agent: Optional[GatewayAgent],
  ) -> None:
    super().__init__(
      is_precompute,
      self.__class__.__qualname__,
      is_debug,
      team_name,
      data_storage_name,
      module_config,
      develop_data,
      finish_post_connect_event,
      gateway_agent,
    )
    self._tactics_center = tactics_center
    self._team_name = team_name
    self._is_precompute = is_precompute
    self._is_debug = is_debug
    self._data_storage_name = data_storage_name
    self._module_config = module_config
    self._develop_data = develop_data

  def post_connect(self) -> None:
    super().post_connect()
    self.precompute_data: PrecomputeData = PrecomputeData(self._data_storage_name)

    self._logger = get_agent_logger(
      f"{self.__class__.__module__}.{self.__class__.__qualname__}",
      self._agent_info,
    )

    self._module_manager: ModuleManager = ModuleManager(
      self._agent_info,
      self._world_info,
      self._scenario_info,
      self._module_config,
      self._develop_data,
    )

    self._message_manager.set_channel_subscriber(
      self._module_manager.get_channel_subscriber(
        "MessageManager.PlatoonChannelSubscriber",
        "adf_core_python.implement.module.communication.default_channel_subscriber.DefaultChannelSubscriber",
      )
    )
    self._message_manager.set_message_coordinator(
      self._module_manager.get_message_coordinator(
        "MessageManager.PlatoonMessageCoordinator",
        "adf_core_python.implement.module.communication.default_message_coordinator.DefaultMessageCoordinator",
      )
    )

    self._tactics_center.initialize(
      self._agent_info,
      self._world_info,
      self._scenario_info,
      self._module_manager,
      self._precompute_data,
      self._message_manager,
      self._develop_data,
    )

    match self._scenario_info.get_mode():
      case Mode.PRECOMPUTATION:
        self._tactics_center.precompute(
          self._agent_info,
          self._world_info,
          self._scenario_info,
          self._module_manager,
          self._precompute_data,
          self._message_manager,
          self._develop_data,
        )
      case Mode.PRECOMPUTED:
        self._tactics_center.resume(
          self._agent_info,
          self._world_info,
          self._scenario_info,
          self._module_manager,
          self._precompute_data,
          self._message_manager,
          self._develop_data,
        )
      case Mode.NON_PRECOMPUTE:
        self._tactics_center.prepare(
          self._agent_info,
          self._world_info,
          self._scenario_info,
          self._module_manager,
          self.precompute_data,
          self._develop_data,
        )

  def think(self) -> None:
    self._tactics_center.think(
      self._agent_info,
      self._world_info,
      self._scenario_info,
      self._module_manager,
      self._precompute_data,
      self._message_manager,
      self._develop_data,
    )
    self.send_msg(
      ActionRest()
      .get_command(self.agent_id, self._agent_info.get_time())
      .to_message_proto()
    )
