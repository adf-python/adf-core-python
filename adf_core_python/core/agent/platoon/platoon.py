from rcrs_core.agents.agent import Agent
from rcrs_core.commands.Command import Command
from rcrs_core.config.config import Config as RCRSConfig
from rcrs_core.worldmodel.changeSet import ChangeSet

from adf_core_python.core.agent.action.action import Action
from adf_core_python.core.agent.communication.message_manager import MessageManager
from adf_core_python.core.agent.config.module_config import ModuleConfig
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.info.agent_info import AgentInfo
from adf_core_python.core.agent.info.scenario_info import Mode, ScenarioInfo
from adf_core_python.core.agent.info.world_info import WorldInfo
from adf_core_python.core.agent.module.module_manager import ModuleManager
from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData
from adf_core_python.core.component.tactics.tactics_agent import TacticsAgent
from adf_core_python.core.config.config import Config
from adf_core_python.core.logger.logger import get_agent_logger


class Platoon(Agent):
    def __init__(
        self,
        tactics_agent: TacticsAgent,
        team_name: str,
        is_precompute: bool,
        is_debug: bool,
        data_storage_name: str,
        module_config: ModuleConfig,
        develop_data: DevelopData,
    ) -> None:
        super().__init__(
            is_precompute,
        )
        self._tactics_agent = tactics_agent
        self._team_name = team_name
        self._is_precompute = is_precompute
        self._is_debug = is_debug
        self._data_storage_name = data_storage_name
        self._module_config = module_config
        self._develop_data = develop_data

    def post_connect(self) -> None:
        self._agent_info: AgentInfo = AgentInfo(self, self.world_model)
        self._world_info: WorldInfo = WorldInfo(self.world_model)
        self._precompute_data: PrecomputeData = PrecomputeData(self._data_storage_name)

        self._logger = get_agent_logger(
            f"{self.__class__.__module__}.{self.__class__.__qualname__}",
            self._agent_info,
        )

        if self._is_precompute:
            self._mode = Mode.PRECOMPUTATION
        else:
            # if self._precompute_data.is_ready():
            #     self._mode = Mode.PRECOMPUTED
            # else:
            #     self._mode = Mode.NON_PRECOMPUTE
            self._mode = Mode.NON_PRECOMPUTE

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

        self._scenario_info: ScenarioInfo = ScenarioInfo(config, self._mode)
        self._module_manager: ModuleManager = ModuleManager(
            self._agent_info,
            self._world_info,
            self._scenario_info,
            self._module_config,
            self._develop_data,
        )

        self._tactics_agent.initialize(
            self._agent_info,
            self._world_info,
            self._scenario_info,
            self._module_manager,
            self._precompute_data,
            MessageManager(),
            self._develop_data,
        )

        match self._mode:
            case Mode.PRECOMPUTATION:
                pass
            case Mode.PRECOMPUTED:
                pass
            case Mode.NON_PRECOMPUTE:
                self._tactics_agent.prepare(
                    self._agent_info,
                    self._world_info,
                    self._scenario_info,
                    self._module_manager,
                    self._precompute_data,
                    self._develop_data,
                )

    def think(self, time: int, change_set: ChangeSet, hear: list[Command]) -> None:
        self._agent_info.set_change_set(change_set)
        self._world_info.set_change_set(change_set)
        self._agent_info.set_time(time)
        self._agent_info.set_heard_commands(hear)

        action: Action = self._tactics_agent.think(
            self._agent_info,
            self._world_info,
            self._scenario_info,
            self._module_manager,
            self._precompute_data,
            MessageManager(),
            self._develop_data,
        )
        if action is not None and self.agent_id is not None:
            self._agent_info.set_executed_action(time, action)
            self.send_msg(action.get_command(self.agent_id, time).prepare_cmd())
