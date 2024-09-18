from rcrs_core.entities.entity import Entity

from adf_core_python.core.agent.config.module_config import ModuleConfig
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.info.scenario_info import Mode
from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData


class Agent(Entity):
    def __init__(
        self,
        team_name: str,
        is_precompute: bool,
        is_debug: bool,
        data_storage_name: str,
        module_config: ModuleConfig,
        develop_data: DevelopData,
    ):
        self._tema_name = team_name
        self._is_precompute = is_precompute
        self._is_debug = is_debug

        if self._is_precompute:
            # PrecomputeData.remove_data(data_storage_name)
            self._mode = Mode.PRECOMPUTATION

        self._module_config: ModuleConfig = module_config
        self._develop_data: DevelopData = develop_data
        self._precompute_data: PrecomputeData = PrecomputeData(data_storage_name)
        self._message_manager = None
