from threading import Event

from rcrs_core.connection.URN import Entity as EntityURN

from adf_core_python.core.agent.config.module_config import ModuleConfig
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.platoon.platoon import Platoon
from adf_core_python.core.component.tactics.tactics_agent import TacticsAgent


class PlatoonPolice(Platoon):
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
        )

    def precompute(self) -> None:
        pass

    def get_requested_entities(self) -> list[EntityURN]:
        return [EntityURN.POLICE_FORCE]
