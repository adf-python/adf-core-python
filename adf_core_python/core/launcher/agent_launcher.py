import importlib
import threading
import time

from adf_core_python.core.component.abstract_loader import AbstractLoader
from adf_core_python.core.config.config import Config
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
        self.thread_list: list[threading.Thread] = []

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
        host: str = self.config.get_value(ConfigKey.KEY_KERNEL_HOST, "localhost")
        port: int = self.config.get_value(ConfigKey.KEY_KERNEL_PORT, 27931)
        self.logger.info(f"Start agent launcher (host: {host}, port: {port})")

        component_launcher: ComponentLauncher = ComponentLauncher(
            host, port, self.logger
        )

        for connector in self.connectors:
            threads = connector.connect(component_launcher, self.config, self.loader)
            for thread in threads:
                thread.daemon = True
                thread.start()
                time.sleep(0.5)
            self.thread_list.extend(threads)

        for thread in self.thread_list:
            thread.join()
