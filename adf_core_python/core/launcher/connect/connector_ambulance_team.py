import threading

from adf_core_python.core.agent.config.module_config import ModuleConfig
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.platoon.platoon_ambulance import PlatoonAmbulance
from adf_core_python.core.component.abstract_loader import AbstractLoader
from adf_core_python.core.component.tactics.tactics_ambulance_team import (
    TacticsAmbulanceTeam,
)
from adf_core_python.core.config.config import Config
from adf_core_python.core.launcher.config_key import ConfigKey
from adf_core_python.core.launcher.connect.component_launcher import ComponentLauncher
from adf_core_python.core.launcher.connect.connector import Connector
from adf_core_python.core.logger.logger import get_logger


class ConnectorAmbulanceTeam(Connector):
    def __init__(self) -> None:
        super().__init__()
        self.logger = get_logger(__name__)

    def connect(
        self,
        component_launcher: ComponentLauncher,
        config: Config,
        loader: AbstractLoader,
    ) -> dict[threading.Thread, threading.Event]:
        count: int = config.get_value(ConfigKey.KEY_AMBULANCE_TEAM_COUNT, 0)
        if count == 0:
            return {}

        threads: dict[threading.Thread, threading.Event] = {}

        for _ in range(count):
            if loader.get_tactics_ambulance_team() is None:
                self.logger.error("Cannot load ambulance team tactics")

            tactics_ambulance_team: TacticsAmbulanceTeam = (
                loader.get_tactics_ambulance_team()
            )

            module_config: ModuleConfig = ModuleConfig(
                config.get_value(
                    ConfigKey.KEY_MODULE_CONFIG_FILE_NAME,
                    ModuleConfig.DEFAULT_CONFIG_FILE_NAME,
                )
            )

            develop_data: DevelopData = DevelopData(
                config.get_value(ConfigKey.KEY_DEBUG_FLAG, False),
                config.get_value(
                    ConfigKey.KEY_DEVELOP_DATA_FILE_NAME, DevelopData.DEFAULT_FILE_NAME
                ),
            )

            request_id: int = component_launcher.generate_request_id()
            finish_post_connect_event = threading.Event()
            thread = threading.Thread(
                target=component_launcher.connect,
                args=(
                    PlatoonAmbulance(
                        tactics_ambulance_team,
                        "ambulance_team",
                        config.get_value(ConfigKey.KEY_PRECOMPUTE, False),
                        config.get_value(ConfigKey.KEY_DEBUG_FLAG, False),
                        "test",
                        module_config,
                        develop_data,
                    ),
                    request_id,
                ),
                name=f"AmbulanceTeam-{request_id}",
            )
            threads[thread] = finish_post_connect_event

        self.logger.info("Connected ambulance team (count: %d)" % count)
        return threads
