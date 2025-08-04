import importlib
import socket
import threading
from typing import Optional

from adf_core_python.core.component.abstract_loader import AbstractLoader
from adf_core_python.core.config.config import Config
from adf_core_python.core.gateway.gateway_launcher import GatewayLauncher
from adf_core_python.core.launcher.config_key import ConfigKey
from adf_core_python.core.launcher.connect.component_launcher import ComponentLauncher
from adf_core_python.core.launcher.connect.connector import Connector
from adf_core_python.core.launcher.connect.connector_ambulance_center import (
  ConnectorAmbulanceCenter,
)
from adf_core_python.core.launcher.connect.connector_ambulance_team import (
  ConnectorAmbulanceTeam,
)
from adf_core_python.core.launcher.connect.connector_fire_brigade import (
  ConnectorFireBrigade,
)
from adf_core_python.core.launcher.connect.connector_fire_station import (
  ConnectorFireStation,
)
from adf_core_python.core.launcher.connect.connector_police_force import (
  ConnectorPoliceForce,
)
from adf_core_python.core.launcher.connect.connector_police_office import (
  ConnectorPoliceOffice,
)
from adf_core_python.core.logger.logger import get_logger


class AgentLauncher:
  def __init__(self, config: Config):
    self.config = config
    self.logger = get_logger(__name__)
    self.connectors: list[Connector] = []
    self.agent_thread_list: list[threading.Thread] = []

  def init_connector(self) -> None:
    loader_name, loader_class_name = self.config.get_value(
      ConfigKey.KEY_LOADER_CLASS,
      "adf_core_python.implement.default_loader.DefaultLoader",
    ).rsplit(".", 1)
    loader_module = importlib.import_module(loader_name)
    self.loader: AbstractLoader = getattr(
      loader_module,
      loader_class_name,
    )(
      self.config.get_value(ConfigKey.KEY_TEAM_NAME),
    )

    self.connectors.append(ConnectorAmbulanceTeam())
    self.connectors.append(ConnectorAmbulanceCenter())
    self.connectors.append(ConnectorFireBrigade())
    self.connectors.append(ConnectorFireStation())
    self.connectors.append(ConnectorPoliceForce())
    self.connectors.append(ConnectorPoliceOffice())

  def launch(self) -> None:
    kernel_host: str = self.config.get_value(ConfigKey.KEY_KERNEL_HOST, "localhost")
    kernel_port: int = self.config.get_value(ConfigKey.KEY_KERNEL_PORT, 27931)

    component_launcher: ComponentLauncher = ComponentLauncher(
      kernel_host, kernel_port, self.logger
    )
    timeout: int = self.config.get_value(
      ConfigKey.KEY_KERNEL_TIMEOUT,
      30,
    )
    if component_launcher.check_kernel_connection(timeout=timeout):
      self.logger.info(f"Kernel is running (host: {kernel_host}, port: {kernel_port})")
    else:
      self.logger.error(
        f"Kernel is not running (host: {kernel_host}, port: {kernel_port})"
      )
      return

    self.logger.info(f"Start agent launcher (host: {kernel_host}, port: {kernel_port})")

    gateway_launcher: Optional[GatewayLauncher] = None
    gateway_flag: bool = self.config.get_value(ConfigKey.KEY_GATEWAY_FLAG, False)
    if gateway_flag:
      gateway_host: str = self.config.get_value(ConfigKey.KEY_GATEWAY_HOST, "localhost")
      gateway_port: int = self.config.get_value(ConfigKey.KEY_GATEWAY_PORT, 27941)
      self.logger.info(
        f"Start gateway launcher (host: {gateway_host}, port: {gateway_port})"
      )

      gateway_launcher = GatewayLauncher(gateway_host, gateway_port, self.logger)

    connector_thread_list: list[threading.Thread] = []
    for connector in self.connectors:
      threads = connector.connect(
        component_launcher, gateway_launcher, self.config, self.loader
      )
      self.agent_thread_list.extend(threads)

      def connect() -> None:
        for thread, event in threads.items():
          thread.daemon = True
          thread.start()
          event.wait(5)

      connector_thread = threading.Thread(target=connect)
      connector_thread_list.append(connector_thread)
      connector_thread.start()

    for thread in connector_thread_list:
      thread.join()

    self.logger.info("All agents have been launched")

    for thread in self.agent_thread_list:
      thread.join()

  def check_kernel_connection(self, host: str, port: int, timeout: int = 5) -> bool:
    try:
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.settimeout(timeout)
      result = sock.connect_ex((host, port))
      sock.close()
      return result == 0
    except Exception as e:
      self.logger.error(f"カーネルへの接続確認中にエラーが発生しました: {e}")
      return False
