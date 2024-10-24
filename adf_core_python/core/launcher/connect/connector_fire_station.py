import threading
from logging import Logger, getLogger

from rcrs_core.agents.fireStationAgent import FireStationAgent
from rcrs_core.connection.componentLauncher import ComponentLauncher

from adf_core_python.core.agent.config.module_config import ModuleConfig
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.component.abstract_loader import AbstractLoader
from adf_core_python.core.config.config import Config
from adf_core_python.core.launcher.config_key import ConfigKey
from adf_core_python.core.launcher.connect.connector import Connector


class ConnectorFireStation(Connector):
    def __init__(self) -> None:
        super().__init__()
        self.logger: Logger = getLogger(__name__)

    def connect(
        self,
        component_launcher: ComponentLauncher,
        config: Config,
        loader: AbstractLoader,
    ) -> list[threading.Thread]:
        count: int = config.get_value(ConfigKey.KEY_FIRE_STATION_COUNT, 0)
        if count == 0:
            return []

        threads: list[threading.Thread] = []

        for _ in range(count):
            # tactics_fire_station: TacticsFireStation
            if loader.get_tactics_fire_station() is not None:
                self.logger.error("Cannot load fire station tactics")
                # tactics_fire_station = loader.get_tactics_fire_station()
            else:
                # tactics_fire_station = DummyTacticsFireStation()
                pass

            module_config: ModuleConfig = ModuleConfig(  # noqa: F841
                config.get_value(
                    ConfigKey.KEY_MODULE_CONFIG_FILE_NAME,
                    ModuleConfig.DEFAULT_CONFIG_FILE_NAME,
                )
            )

            develop_data: DevelopData = DevelopData(  # noqa: F841
                config.get_value(ConfigKey.KEY_DEBUG_FLAG, False),
                config.get_value(
                    ConfigKey.KEY_DEVELOP_DATA_FILE_NAME, DevelopData.DEFAULT_FILE_NAME
                ),
            )

            # TODO: component_launcher.generate_request_ID can cause race condition
            thread = threading.Thread(
                target=component_launcher.connect,
                args=(
                    FireStationAgent(
                        config.get_value(ConfigKey.KEY_PRECOMPUTE, False),
                    ),  # type: ignore
                    component_launcher.generate_request_ID(),
                ),
            )
            threads.append(thread)

        self.logger.info("Connected fire station (count: %d)" % count)
        return threads
