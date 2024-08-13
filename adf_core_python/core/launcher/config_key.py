from typing import Final


class ConfigKey:
    # General
    KEY_LOADER_CLASS: Final[str] = "adf.launcher.loader"
    KEY_KERNEL_HOST: Final[str] = "kernel.host"
    KEY_KERNEL_PORT: Final[str] = "kernel.port"
    KEY_TEAM_NAME: Final[str] = "team.name"
    KEY_DEBUG_FLAG: Final[str] = "adf.debug.flag"
    KEY_DEVELOP_FLAG: Final[str] = "adf.develop.flag"
    KEY_DEVELOP_DATA_FILE_NAME: Final[str] = "adf.develop.filename"
    KEY_DEVELOP_DATA: Final[str] = "adf.develop.data"
    KEY_MODULE_CONFIG_FILE_NAME: Final[str] = "adf.agent.moduleconfig.filename"
    KEY_MODULE_DATA: Final[str] = "adf.agent.moduleconfig.data"
    KEY_PRECOMPUTE: Final[str] = "adf.launcher.precompute"
    # Platoon
    KEY_AMBULANCE_TEAM_COUNT: Final[str] = "adf.team.platoon.ambulance.count"
    KEY_FIRE_BRIGADE_COUNT: Final[str] = "adf.team.platoon.fire.count"
    KEY_POLICE_FORCE_COUNT: Final[str] = "adf.team.platoon.police.count"
    # Office
    KEY_AMBULANCE_CENTRE_COUNT: Final[str] = "adf.team.office.ambulance.count"
    KEY_FIRE_STATION_COUNT: Final[str] = "adf.team.office.fire.count"
    KEY_POLICE_OFFICE_COUNT: Final[str] = "adf.team.office.police.count"
