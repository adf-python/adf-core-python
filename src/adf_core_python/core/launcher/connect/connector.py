from __future__ import annotations

import threading
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
  from adf_core_python.core.component import AbstractLoader
  from adf_core_python.core.config import Config
  from adf_core_python.core.gateway import GatewayLauncher
  from adf_core_python.core.launcher.connect import ComponentLauncher


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
