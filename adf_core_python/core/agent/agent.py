from abc import abstractmethod

from rcrs_core.agents.agent import Agent as RCRSAgent
from rcrs_core.connection.URN import Entity as EntityURN

from adf_core_python.core.agent.communication.message_manager import MessageManager
from adf_core_python.core.agent.config.module_config import ModuleConfig
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.info.scenario_info import Mode
from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData


class Agent(RCRSAgent):
    def __init__(
        self,
        is_precompute: bool,
        is_debug: bool,
        team_name: str,
        deta_storage_name: str,
        module_config: ModuleConfig,
        develop_data: DevelopData,
    ) -> None:
        super().__init__(is_precompute)
        self.team_name = team_name
        self.is_debug = is_debug
        self.is_precompute = is_precompute

        if is_precompute:
            # PrecomputeData.remove_date(deta_storage_name)
            self.mode = Mode.PRECOMPUTATION

        self.module_config = module_config
        self.develop_data = develop_data
        self.precompute_data = PrecomputeData(deta_storage_name)
        self.message_manager: MessageManager = MessageManager()

    def precompute(self):
        pass

    @abstractmethod
    def get_requested_entities(self) -> list[EntityURN]:
        pass
