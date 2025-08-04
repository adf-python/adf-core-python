import threading
from typing import Optional

from adf_core_python.core.agent.config.module_config import ModuleConfig
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.office.office_ambulance import OfficeAmbulance
from adf_core_python.core.component.abstract_loader import AbstractLoader
from adf_core_python.core.component.tactics.tactics_ambulance_center import (
    TacticsAmbulanceCenter,
)
from adf_core_python.core.config.config import Config
from adf_core_python.core.gateway.gateway_agent import GatewayAgent
from adf_core_python.core.gateway.gateway_launcher import GatewayLauncher
from adf_core_python.core.launcher.config_key import ConfigKey
from adf_core_python.core.launcher.connect.component_launcher import ComponentLauncher
from adf_core_python.core.launcher.connect.connector import Connector
from adf_core_python.core.logger.logger import get_logger


class ConnectorAmbulanceCenter(Connector):
    def __init__(self) -> None:
        super().__init__()
        self.logger = get_logger(__name__)

    def connect(
        self,
        component_launcher: ComponentLauncher,
        gateway_launcher: Optional[GatewayLauncher],
        config: Config,
        loader: AbstractLoader,
    ) -> dict[threading.Thread, threading.Event]:
        count: int = config.get_value(ConfigKey.KEY_AMBULANCE_CENTRE_COUNT, 0)
        if count == 0:
            return {}

        threads: dict[threading.Thread, threading.Event] = {}

        for _ in range(count):
            if loader.get_tactics_ambulance_center() is None:
                self.logger.error("Cannot load ambulance centre tactics")

            tactics_ambulance_center: TacticsAmbulanceCenter = (
                loader.get_tactics_ambulance_center()
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

            precompute_data_dir: str = f"{config.get_value(ConfigKey.KEY_PRECOMPUTE_DATA_DIR, 'precompute')}/ambulance_center"

            finish_post_connect_event = threading.Event()
            request_id: int = component_launcher.generate_request_id()

            gateway_agent: Optional[GatewayAgent] = None
            if isinstance(gateway_launcher, GatewayLauncher):
                gateway_agent = GatewayAgent(gateway_launcher)
                if isinstance(gateway_agent, GatewayAgent):
                    gateway_thread = threading.Thread(
                        target=gateway_launcher.connect,
                        args=(gateway_agent,),
                    )
                    gateway_thread.daemon = True
                    gateway_thread.start()

            component_thread = threading.Thread(
                target=component_launcher.connect,
                args=(
                    OfficeAmbulance(
                        tactics_ambulance_center,
                        "ambulance_center",
                        config.get_value(ConfigKey.KEY_PRECOMPUTE, False),
                        config.get_value(ConfigKey.KEY_DEBUG_FLAG, False),
                        precompute_data_dir,
                        module_config,
                        develop_data,
                        finish_post_connect_event,
                        gateway_agent,
                    ),
                    request_id,
                ),
                name=f"AmbulanceCenterAgent-{request_id}",
            )
            threads[component_thread] = finish_post_connect_event

        return threads
