from rcrs_core.connection.URN import Entity as EntityURN

from adf_core_python.core.agent.config.module_config import ModuleConfig
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.office.office import Office
from adf_core_python.core.component.tactics.tactics_center import TacticsCenter


class OfficePolice(Office):
    def __init__(
        self,
        tactics_center: TacticsCenter,
        team_name: str,
        is_precompute: bool,
        is_debug: bool,
        data_storage_name: str,
        module_config: ModuleConfig,
        develop_data: DevelopData,
    ) -> None:
        super().__init__(
            tactics_center,
            team_name,
            is_precompute,
            is_debug,
            data_storage_name,
            module_config,
            develop_data,
        )

    def precompute(self) -> None:
        pass

    def get_requested_entities(self) -> list[EntityURN]:
        return [EntityURN.POLICE_OFFICE]
