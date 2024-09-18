from abc import ABC, abstractmethod

from rcrs_core.connection.componentLauncher import ComponentLauncher

from adf_core_python.core.component.abstract_loader import AbstractLoader
from adf_core_python.core.config.config import Config


class Connector(ABC):
    def __init__(self) -> None:
        self.connected_agent_count = 0

    @abstractmethod
    def connect(
        self,
        component_launcher: ComponentLauncher,
        config: Config,
        loader: AbstractLoader,
    ) -> None:
        raise NotImplementedError

    def get_connected_agent_count(self) -> int:
        return self.connected_agent_count
