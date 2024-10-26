import sys
from abc import abstractmethod
from typing import Any, NoReturn

from rcrs_core.agents.agent import Agent as RCRSAgent
from rcrs_core.connection.URN import Entity as EntityURN
from rcrs_core.worldmodel.worldmodel import WorldModel

from adf_core_python.core.agent.communication.message_manager import MessageManager
from adf_core_python.core.agent.config.module_config import ModuleConfig
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.info.scenario_info import Mode
from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData
from adf_core_python.core.logger.logger import get_logger


class Agent(RCRSAgent):
    def __init__(
        self,
        is_precompute: bool,
        name: str,
        is_debug: bool,
        team_name: str,
        deta_storage_name: str,
        module_config: ModuleConfig,
        develop_data: DevelopData,
    ) -> None:
        self.name = name
        self.connect_request_id = None
        self.world_model = WorldModel()
        self.config = None
        self.random = None
        self.agent_id = None
        self.precompute_flag = is_precompute
        self.logger = get_logger(
            f"{self.__class__.__module__}.{self.__class__.__qualname__}"
        )

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

    def handle_connect_error(self, msg: Any) -> NoReturn:
        self.logger.error(
            "Failed to connect agent: %s(request_id: %s)", msg.reason, msg.request_id
        )
        sys.exit(1)

    def precompute(self):
        pass

    @abstractmethod
    def get_requested_entities(self) -> list[EntityURN]:
        pass
