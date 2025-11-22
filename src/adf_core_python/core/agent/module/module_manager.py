from __future__ import annotations

import importlib
from typing import TYPE_CHECKING, Any, Optional

from adf_core_python.core.component.action import ExtendAction
from adf_core_python.core.component.centralized import CommandExecutor, CommandPicker
from adf_core_python.core.component.communication import (
  ChannelSubscriber,
  MessageCoordinator,
)
from adf_core_python.core.component.module import AbstractModule
from adf_core_python.core.gateway import GatewayAgent, GatewayModule, ModuleDict
from adf_core_python.core.gateway.component.module import (
  GatewayAbstractModule,
)
from adf_core_python.core.logger import get_agent_logger

if TYPE_CHECKING:
  from adf_core_python.core.agent.config import ModuleConfig
  from adf_core_python.core.agent.develop import DevelopData
  from adf_core_python.core.agent.info import AgentInfo, ScenarioInfo, WorldInfo


class ModuleManager:
  def __init__(
    self,
    agent_info: AgentInfo,
    world_info: WorldInfo,
    scenario_info: ScenarioInfo,
    module_config: ModuleConfig,
    develop_data: DevelopData,
    gateway_agent: Optional[GatewayAgent] = None,
  ) -> None:
    self._agent_info = agent_info
    self._world_info = world_info
    self._scenario_info = scenario_info
    self._module_config = module_config
    self._develop_data = develop_data
    self._gateway_agent = gateway_agent
    self._modules: dict[str, AbstractModule] = {}
    self._actions: dict[str, ExtendAction] = {}

    self._executors: dict[str, Any] = {}
    self._pickers: dict[str, Any] = {}
    self._channel_subscribers: dict[str, Any] = {}
    self._message_coordinators: dict[str, Any] = {}

    self._module_dict: ModuleDict = ModuleDict()

    self._logger = get_agent_logger(
      f"{self.__class__.__module__}.{self.__class__.__qualname__}",
      self._agent_info,
    )

  def get_module(
    self, module_name: str, default_module_class_name: str
  ) -> AbstractModule:
    instance = self._modules.get(module_name)
    if instance is not None:
      return instance

    class_name = self._module_config.get_value(module_name)
    if class_name is None:
      self._logger.warning(
        f"Module {module_name} not found in config. Using default module {default_module_class_name}"
      )

    if class_name is not None:
      try:
        module_class: type = self._load_module(class_name)
        if issubclass(module_class, AbstractModule):
          instance = module_class(
            self._agent_info,
            self._world_info,
            self._scenario_info,
            self,
            self._develop_data,
          )
          self._modules[module_name] = instance
          return instance
      except ModuleNotFoundError:
        self._logger.warning(
          f"Module {module_name} not found in python. "
          f"If gateway flag is active, using module {module_name} in java"
        )

      if isinstance(self._gateway_agent, GatewayAgent):
        gateway_module = GatewayModule(self._gateway_agent)
        java_class_name = gateway_module.initialize(module_name, "")
        class_name = self._module_dict[java_class_name]
        if class_name is not None:
          module_class = self._load_module(class_name)
          if issubclass(module_class, GatewayAbstractModule):
            instance = module_class(
              self._agent_info,
              self._world_info,
              self._scenario_info,
              self,
              self._develop_data,
              gateway_module,
            )
            self._modules[module_name] = instance
            return instance

    class_name = default_module_class_name
    if class_name is not None:
      module_class = self._load_module(class_name)
      if issubclass(module_class, AbstractModule):
        instance = module_class(
          self._agent_info,
          self._world_info,
          self._scenario_info,
          self,
          self._develop_data,
        )
        self._modules[module_name] = instance
        return instance

    raise RuntimeError(f"Module {class_name} is not a subclass of AbstractModule")

  def get_extend_action(
    self, action_name: str, default_action_class_name: str
  ) -> ExtendAction:
    class_name = self._module_config.get_value(action_name)
    if class_name is None:
      self._logger.warning(
        f"Action {action_name} not found in config. Using default action {default_action_class_name}"
      )
      class_name = default_action_class_name

    action_class: type = self._load_module(class_name)

    instance = self._actions.get(action_name)
    if instance is not None:
      return instance

    if issubclass(action_class, ExtendAction):
      instance = action_class(
        self._agent_info,
        self._world_info,
        self._scenario_info,
        self,
        self._develop_data,
      )
      self._actions[action_name] = instance
      return instance

    raise RuntimeError(f"Action {class_name} is not a subclass of ExtendAction")

  def get_channel_subscriber(
    self, channel_subscriber_name: str, default_channel_subscriber_name: str
  ) -> ChannelSubscriber:
    class_name = self._module_config.get_value(channel_subscriber_name)
    if class_name is None:
      self._logger.warning(
        f"Channel subscriber {channel_subscriber_name} not found in config. Using default channel subscriber {default_channel_subscriber_name}"
      )
      class_name = default_channel_subscriber_name

    channel_subscriber_class: type = self._load_module(class_name)

    instance = self._channel_subscribers.get(channel_subscriber_name)
    if instance is not None:
      return instance

    if issubclass(channel_subscriber_class, ChannelSubscriber):
      instance = channel_subscriber_class()
      self._channel_subscribers[channel_subscriber_name] = instance
      return instance

    raise RuntimeError(
      f"Channel subscriber {class_name} is not a subclass of ChannelSubscriber"
    )

  def get_message_coordinator(
    self, message_coordinator_name: str, default_message_coordinator_name: str
  ) -> MessageCoordinator:
    class_name = self._module_config.get_value(message_coordinator_name)
    if class_name is None:
      self._logger.warning(
        f"Channel subscriber {message_coordinator_name} not found in config. Using default channel subscriber {default_message_coordinator_name}"
      )
      class_name = default_message_coordinator_name

    message_coordinator_class: type = self._load_module(class_name)

    instance = self._message_coordinators.get(message_coordinator_name)
    if instance is not None:
      return instance

    if issubclass(message_coordinator_class, MessageCoordinator):
      instance = message_coordinator_class()
      self._message_coordinators[message_coordinator_name] = instance
      return instance

    raise RuntimeError(
      f"Message coordinator {class_name} is not a subclass of MessageCoordinator"
    )

  def get_command_executor(
    self, command_executor_name: str, default_command_executor_name: str
  ) -> CommandExecutor:
    class_name = self._module_config.get_value(command_executor_name)
    if class_name is None:
      self._logger.warning(
        f"Command executor {command_executor_name} not found in config. Using default command executor {default_command_executor_name}"
      )
      class_name = default_command_executor_name

    command_executor_class: type = self._load_module(class_name)

    instance = self._executors.get(command_executor_name)
    if instance is not None:
      return instance

    if issubclass(command_executor_class, CommandExecutor):
      instance = command_executor_class(
        self._agent_info,
        self._world_info,
        self._scenario_info,
        self,
        self._develop_data,
      )
      self._executors[command_executor_name] = instance
      return instance

    raise RuntimeError(f"Command executor {class_name} is not a subclass of object")

  def get_command_picker(
    self, command_picker_name: str, default_command_picker_name: str
  ) -> CommandPicker:
    class_name = self._module_config.get_value(command_picker_name)
    if class_name is None:
      self._logger.warning(
        f"Command picker {command_picker_name} not found in config. Using default command picker {default_command_picker_name}"
      )
      class_name = default_command_picker_name

    command_picker_class: type = self._load_module(class_name)

    instance = self._pickers.get(command_picker_name)
    if instance is not None:
      return instance

    if issubclass(command_picker_class, CommandPicker):
      instance = command_picker_class(
        self._agent_info,
        self._world_info,
        self._scenario_info,
        self,
        self._develop_data,
      )
      self._pickers[command_picker_name] = instance
      return instance

    raise RuntimeError(f"Command picker {class_name} is not a subclass of object")

  def _load_module(self, class_name: str) -> type:
    module_name, module_class_name = class_name.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, module_class_name)
