import sys
from abc import abstractmethod
from typing import Any, NoReturn

from rcrs_core.agents.agent import Agent as RCRSAgent
from rcrs_core.commands.Command import Command
from rcrs_core.config.config import Config as RCRSConfig
from rcrs_core.connection.URN import Entity as EntityURN
from rcrs_core.worldmodel.changeSet import ChangeSet
from rcrs_core.worldmodel.worldmodel import WorldModel

from adf_core_python.core.agent.communication.message_manager import MessageManager
from adf_core_python.core.agent.communication.standard.standard_communication_module import (
    StandardCommunicationModule,
)
from adf_core_python.core.agent.config.module_config import ModuleConfig
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.info.agent_info import AgentInfo
from adf_core_python.core.agent.info.scenario_info import Mode, ScenarioInfo
from adf_core_python.core.agent.info.world_info import WorldInfo
from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData
from adf_core_python.core.component.communication.communication_module import (
    CommunicationModule,
)
from adf_core_python.core.config.config import Config
from adf_core_python.core.launcher.config_key import ConfigKey
from adf_core_python.core.logger.logger import get_agent_logger, get_logger


class Agent(RCRSAgent):
    def __init__(
        self,
        is_precompute: bool,
        name: str,
        is_debug: bool,
        team_name: str,
        data_storage_name: str,
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
            # PrecomputeData.remove_date(data_storage_name)
            self.mode = Mode.PRECOMPUTATION

        self.module_config = module_config
        self.develop_data = develop_data
        self.precompute_data = PrecomputeData(data_storage_name)
        self.message_manager: MessageManager = MessageManager()
        self.communication_module: CommunicationModule = StandardCommunicationModule()

    def post_connect(self) -> None:
        self.world_model.index_entities()

        config = Config()
        if self.config is not None:
            rcrc_config: RCRSConfig = self.config
            for key, value in rcrc_config.data.items():
                config.set_value(key, value)
            for key, value in rcrc_config.int_data.items():
                config.set_value(key, value)
            for key, value in rcrc_config.float_data.items():
                config.set_value(key, value)
            for key, value in rcrc_config.boolean_data.items():
                config.set_value(key, value)
            for key, value in rcrc_config.array_data.items():
                config.set_value(key, value)

        if self.is_precompute:
            self._mode = Mode.PRECOMPUTATION
        else:
            # if self._precompute_data.is_ready():
            #     self._mode = Mode.PRECOMPUTED
            # else:
            #     self._mode = Mode.NON_PRECOMPUTE
            self._mode = Mode.NON_PRECOMPUTE

        config.set_value(ConfigKey.KEY_DEBUG_FLAG, self.is_debug)
        config.set_value(
            ConfigKey.KEY_DEVELOP_FLAG, self.develop_data.is_develop_mode()
        )
        self.ignore_time = config.get_value("kernel.agents.ignoreuntil", 3)
        self.scenario_info: ScenarioInfo = ScenarioInfo(config, self._mode)
        self.world_info: WorldInfo = WorldInfo(self.world_model)
        self.agent_info = AgentInfo(self, self.world_model)
        self.logger = get_agent_logger(
            f"{self.__class__.__module__}.{self.__class__.__qualname__}",
            self.agent_info,
        )

    def think(self, time: int, change_set: ChangeSet, hear: list[Command]) -> None:
        self.agent_info.record_think_start_time()
        self.agent_info.set_time(time)

        # if time == 1:
        #     self.message_manager.register_message_class()

    def handle_connect_error(self, msg: Any) -> NoReturn:
        self.logger.error(
            "Failed to connect agent: %s(request_id: %s)", msg.reason, msg.request_id
        )
        sys.exit(1)

    def precompute(self) -> None:
        pass

    @abstractmethod
    def get_requested_entities(self) -> list[EntityURN]:
        pass
