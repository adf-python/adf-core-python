import threading
from abc import ABC, abstractmethod
from typing import Optional

from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.component.abstract_loader import AbstractLoader
from adf_core_python.core.config.config import Config
from adf_core_python.core.gateway.gateway_launcher import GatewayLauncher
from adf_core_python.core.launcher.config_key import ConfigKey
from adf_core_python.core.launcher.connect.component_launcher import ComponentLauncher


class Connector(ABC):
  def __init__(self) -> None:
    self.connected_agent_count = 0

  @abstractmethod
  def connect(
    self,
    component_launcher: ComponentLauncher,
    gateway_launcher: Optional[GatewayLauncher],
    config: Config,
    loader: AbstractLoader,
  ) -> dict[threading.Thread, threading.Event]:
    raise NotImplementedError

  def get_connected_agent_count(self) -> int:
    return self.connected_agent_count

  def _create_develop_data(self, config: Config) -> DevelopData:
    return DevelopData(
      config.get_value(ConfigKey.KEY_DEVELOP_FLAG, False),
      config.get_value(
        ConfigKey.KEY_DEVELOP_DATA_FILE_NAME, DevelopData.DEFAULT_FILE_NAME
      ),
    )
