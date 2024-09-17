import importlib
import threading

from rcrs_core.connection.componentLauncher import ComponentLauncher

from adf_core_python.core.component.abstract_loader import AbstractLoader
from adf_core_python.core.config.config import Config
from adf_core_python.core.launcher.config_key import ConfigKey
from adf_core_python.core.launcher.connect.connector import Connector
from adf_core_python.core.launcher.connect.connector_ambulance_centre import (
    ConnectorAmbulanceCentre,
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


class AgentLauncher:
    def __init__(self, config: Config):
        self.config = config
        self.connectors: list[Connector] = []

    def initConnector(self):
        loader_name, loader_class_name = self.config.get_value(
            ConfigKey.KEY_LOADER_CLASS
        ).split(".")
        self.loader: AbstractLoader = importlib.import_module(
            loader_name,
        ).__getattr__(
            loader_class_name,
        )(
            self.config.get_value(ConfigKey.KEY_TEAM_NAME),
        )

        self.connectors.append(ConnectorAmbulanceCentre())
        self.connectors.append(ConnectorAmbulanceTeam())
        self.connectors.append(ConnectorFireBrigade())
        self.connectors.append(ConnectorFireStation())
        self.connectors.append(ConnectorPoliceForce())
        self.connectors.append(ConnectorPoliceOffice())

    def launch(self):
        host: str = self.config.get_value(ConfigKey.KEY_KERNEL_HOST, "localhost")
        port: int = self.config.get_value(ConfigKey.KEY_KERNEL_PORT, 27931)
        component_launcher: ComponentLauncher = ComponentLauncher(port, host)

        thread_list: list[threading.Thread] = []
        for connector in self.connectors:
            thread = threading.Thread(
                target=connector.connect,
                args=(component_launcher, self.config, self.loader),
            )
            thread.start()
            thread_list.append(thread)

        for thread in thread_list:
            thread.join()

        connected_agent_count = 0
