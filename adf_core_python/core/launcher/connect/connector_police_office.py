import threading

from adf_core_python.core.agent.config.module_config import ModuleConfig
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.office.office_police import OfficePolice
from adf_core_python.core.component.abstract_loader import AbstractLoader
from adf_core_python.core.component.tactics.tactics_police_office import (
    TacticsPoliceOffice,
)
from adf_core_python.core.config.config import Config
from adf_core_python.core.launcher.config_key import ConfigKey
from adf_core_python.core.launcher.connect.component_launcher import ComponentLauncher
from adf_core_python.core.launcher.connect.connector import Connector
from adf_core_python.core.logger.logger import get_logger


class ConnectorPoliceOffice(Connector):
    def __init__(self) -> None:
        super().__init__()
        self.logger = get_logger(__name__)

    def connect(
        self,
        component_launcher: ComponentLauncher,
        config: Config,
        loader: AbstractLoader,
    ) -> dict[threading.Thread, threading.Event]:
        count: int = config.get_value(ConfigKey.KEY_POLICE_OFFICE_COUNT, 0)
        if count == 0:
            return {}

        threads: dict[threading.Thread, threading.Event] = {}

        for _ in range(count):
            if loader.get_tactics_police_office() is None:
                self.logger.error("Cannot load police office tactics")

            tactics_police_office: TacticsPoliceOffice = (
                loader.get_tactics_police_office()
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
                    OfficePolice(
                        tactics_police_office,
                        "police_office",
                        config.get_value(ConfigKey.KEY_PRECOMPUTE, False),
                        config.get_value(ConfigKey.KEY_DEBUG_FLAG, False),
                        "test",
                        module_config,
                        develop_data,
                    ),
                    request_id,
                ),
                name=f"PoliceOfficeAgent-{request_id}",
            )
            threads[thread] = finish_post_connect_event

        self.logger.info("Connected police office (count: %d)" % count)
        return threads
