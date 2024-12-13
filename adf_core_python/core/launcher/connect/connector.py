import threading
from abc import ABC, abstractmethod
from typing import Optional

from adf_core_python.core.component.abstract_loader import AbstractLoader
from adf_core_python.core.config.config import Config
from adf_core_python.core.gateway.gateway_launcher import GatewayLauncher
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
