from logging import Logger, getLogger

from rcrs_core.agents.policeOfficeAgent import PoliceOfficeAgent
from rcrs_core.config.config import Config
from rcrs_core.connection.componentLauncher import ComponentLauncher

from adf_core_python.core.agent.config.module_config import ModuleConfig
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.component.abstract_loader import AbstractLoader
from adf_core_python.core.launcher.config_key import ConfigKey
from adf_core_python.core.launcher.connect.connector import Connector


class ConnectorPoliceOffice(Connector):
    def __init__(self) -> None:
        super().__init__()
        self.logger: Logger = getLogger(__name__)

    def connect(
        self,
        component_launcher: ComponentLauncher,
        config: Config,
        loader: AbstractLoader,
    ) -> None:
        count: int = config.get_int_value_or_default(
            ConfigKey.KEY_AMBULANCE_CENTRE_COUNT, 0
        )
        if count == 0:
            return

        for _ in range(count):
            # tactics_police_office: TacticsPoliceOffice
            if loader.get_tactics_police_office() is not None:
                self.logger.error("Cannot load police office tactics")
                # tactics_police_office = loader.get_tactics_police_office()
            else:
                # tactics_police_office = DummyTacticsPoliceOffice()
                pass

            module_config: ModuleConfig = ModuleConfig(  # noqa: F841
                config.get_value_or_default(
                    ConfigKey.KEY_MODULE_CONFIG_FILE_NAME,
                    ModuleConfig.DEFAULT_CONFIG_FILE_NAME,
                )
            )

            develop_data: DevelopData = DevelopData(  # noqa: F841
                config.get_boolean_value_or_default(ConfigKey.KEY_DEBUG_FLAG, False),
                config.get_value_or_default(
                    ConfigKey.KEY_DEVELOP_DATA_FILE_NAME, DevelopData.DEFAULT_FILE_NAME
                ),
            )

            # TODO: component_launcher.generate_request_ID can cause race condition
            component_launcher.connect(
                PoliceOfficeAgent(
                    config.get_boolean_value_or_default(
                        ConfigKey.KEY_PRECOMPUTE, False
                    ),
                ),
                component_launcher.generate_request_ID(),
            )

        self.logger.info("Connected ambulance centre (count: %d)" % count)
