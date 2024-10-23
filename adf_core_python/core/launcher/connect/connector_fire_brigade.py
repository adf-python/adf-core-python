import threading

from adf_core_python.core.agent.config.module_config import ModuleConfig
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.platoon.platoon_fire import PlatoonFire
from adf_core_python.core.component.abstract_loader import AbstractLoader
from adf_core_python.core.component.tactics.tactics_fire_brigade import (
    TacticsFireBrigade,
)
from adf_core_python.core.config.config import Config
from adf_core_python.core.launcher.config_key import ConfigKey
from adf_core_python.core.launcher.connect.component_launcher import ComponentLauncher
from adf_core_python.core.launcher.connect.connector import Connector
from adf_core_python.core.logger.logger import get_logger


class ConnectorFireBrigade(Connector):
    def __init__(self) -> None:
        super().__init__()
        self.logger = get_logger(__name__)

    def connect(
        self,
        component_launcher: ComponentLauncher,
        config: Config,
        loader: AbstractLoader,
    ) -> list[threading.Thread]:
        count: int = config.get_value(ConfigKey.KEY_FIRE_BRIGADE_COUNT, 0)
        if count == 0:
            return []

        threads: list[threading.Thread] = []

        for _ in range(count):
            if loader.get_tactics_fire_brigade() is None:
                self.logger.error("Cannot load fire brigade tactics")

            tactics_fire_brigade: TacticsFireBrigade = loader.get_tactics_fire_brigade()

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

            thread = threading.Thread(
                target=component_launcher.connect,
                args=(
                    PlatoonFire(
                        tactics_fire_brigade,
                        "fire_brigade",
                        config.get_value(ConfigKey.KEY_PRECOMPUTE, False),
                        config.get_value(ConfigKey.KEY_DEBUG_FLAG, False),
                        "test",
                        module_config,
                        develop_data,
                    ),
                    component_launcher.generate_request_id(),
                ),
            )
            threads.append(thread)

        self.logger.info("Connected fire brigade (count: %d)" % count)
        return threads
