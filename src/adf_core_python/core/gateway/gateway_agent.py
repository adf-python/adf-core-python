from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional

from rcrscore.urn import CommandURN

from adf_core_python.core.gateway.message.am_agent import AMAgent
from adf_core_python.core.gateway.message.am_update import AMUpdate
from adf_core_python.core.gateway.message.ma_exec_response import MAExecResponse
from adf_core_python.core.gateway.message.ma_module_response import (
  MAModuleResponse,
)
from adf_core_python.core.gateway.message.moduleMessageFactory import (
  ModuleMessageFactory,
)
from adf_core_python.core.logger.logger import get_logger

if TYPE_CHECKING:
  from adf_core_python.core.agent.info.world_info import WorldInfo
  from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
  from rcrscore.proto import RCRSProto_pb2
  from adf_core_python.core.agent.info.agent_info import AgentInfo
  from adf_core_python.core.gateway.gateway_launcher import GatewayLauncher
  from adf_core_python.core.gateway.gateway_module import GatewayModule


class GatewayAgent:
  def __init__(self, gateway_launcher: GatewayLauncher) -> None:
    self._gateway_launcher = gateway_launcher
    self.send_msg: Optional[Callable] = None
    self._is_initialized = False
    self._agent_info: Optional[AgentInfo] = None
    self._world_info: Optional[WorldInfo] = None
    self._scenario_info: Optional[ScenarioInfo] = None
    self._gateway_modules: dict[str, GatewayModule] = {}
    self._logger = get_logger(__name__)

  def get_module_count(self) -> int:
    return len(self._gateway_modules)

  def add_gateway_module(self, gateway_module: GatewayModule) -> None:
    self._gateway_modules[gateway_module.get_module_id()] = gateway_module

  def is_initialized(self) -> bool:
    return self._is_initialized

  def set_initialize_data(
    self, agent_info: AgentInfo, world_info: WorldInfo, scenario_info: ScenarioInfo
  ) -> None:
    self._agent_info = agent_info
    self._world_info = world_info
    self._scenario_info = scenario_info

  def initialize(self) -> None:
    if self.send_msg is None:
      raise RuntimeError("send_msg is None")
    if (
      self._agent_info is None
      or self._world_info is None
      or self._scenario_info is None
    ):
      raise RuntimeError(
        "Required variables is None, "
        "You must exec set_initialized_data() before calling initialize()"
      )

    am_agent = AMAgent()
    self.send_msg(
      am_agent.write(
        self._agent_info.get_entity_id(),
        list(self._world_info.get_world_model().get_entities()),
        self._scenario_info.get_config().config,
        int(self._scenario_info.get_mode()),
      )
    )
    self._is_initialized = True

  def update(self) -> None:
    if self.send_msg is None:
      raise RuntimeError("send_msg is None")
    if self._agent_info is None or self._world_info is None:
      raise RuntimeError(
        "Required variables is None, "
        "You must exec set_initialized_data() before calling update()"
      )

    am_update = AMUpdate()
    self.send_msg(
      am_update.write(
        self._agent_info.get_time(),
        self._world_info.get_change_set(),
        self._agent_info.get_heard_commands(),
      )
    )

  def set_send_msg(self, connection_send_func: Callable) -> None:
    self.send_msg = connection_send_func

  def message_received(self, msg: RCRSProto_pb2.MessageProto) -> None:
    c_msg = ModuleMessageFactory().make_message(msg)
    if isinstance(c_msg, MAModuleResponse):
      if c_msg.module_id is None or c_msg.class_name is None:
        raise RuntimeError("Failed to receive message")

      self._gateway_modules[c_msg.module_id].set_gateway_class_name(c_msg.class_name)
      self._gateway_modules[c_msg.module_id].set_is_initialized(True)
    if isinstance(c_msg, MAExecResponse):
      if c_msg.module_id is None:
        raise RuntimeError("Failed to receive message")

      self._gateway_modules[c_msg.module_id].set_execute_response(c_msg.result)
      self._gateway_modules[c_msg.module_id].set_is_executed(True)

    if msg.urn == CommandURN.AK_SPEAK:
      if self.send_msg is None:
        raise RuntimeError("send_msg is None")
      self.send_msg(msg)
