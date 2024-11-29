from rcrs_core.connection.URN import Entity as EntityURN

from adf_core_python.core.agent.office.office import Office


class OfficeFire(Office):
    def __init__(
        self,
        tactics_center,
        team_name,
        is_precompute,
        is_debug,
        data_storage_name,
        module_config,
        develop_data,
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

    def post_connect(self) -> None:
        super().post_connect()

    def get_requested_entities(self) -> list[EntityURN]:
        return [EntityURN.FIRE_STATION]
