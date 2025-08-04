from threading import Event
from typing import Optional

from rcrscore.urn import EntityURN

from adf_core_python.core.agent.config.module_config import ModuleConfig
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.platoon.platoon import Platoon
from adf_core_python.core.component.tactics.tactics_agent import TacticsAgent
from adf_core_python.core.gateway.gateway_agent import GatewayAgent


class PlatoonFire(Platoon):
  def __init__(
    self,
    tactics_agent: TacticsAgent,
    team_name: str,
    is_precompute: bool,
    is_debug: bool,
    data_storage_name: str,
    module_config: ModuleConfig,
    develop_data: DevelopData,
    finish_post_connect_event: Event,
    gateway_agent: Optional[GatewayAgent],
  ):
    super().__init__(
      tactics_agent,
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
    return [EntityURN.FIRE_BRIGADE]
