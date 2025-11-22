from threading import Event
from typing import Optional

from rcrscore.urn import EntityURN

from adf_core_python.core.agent.config import ModuleConfig
from adf_core_python.core.agent.develop import DevelopData
from adf_core_python.core.agent.office import Office
from adf_core_python.core.component.tactics import TacticsCenter
from adf_core_python.core.gateway import GatewayAgent


class OfficeFire(Office):
  def __init__(
    self,
    tactics_center: TacticsCenter,
    team_name: str,
    is_precompute: bool,
    is_debug: bool,
    data_storage_name: str,
    module_config: ModuleConfig,
    develop_data: DevelopData,
    finish_post_connect_event: Event,
    gateway_agent: Optional[GatewayAgent],
  ) -> None:
    super().__init__(
      tactics_center,
      team_name,
      is_precompute,
      is_debug,
      data_storage_name,
      module_config,
      develop_data,
      finish_post_connect_event,
      gateway_agent,
    )

  def get_requested_entities(self) -> list[EntityURN]:
    return [EntityURN.FIRE_STATION]
