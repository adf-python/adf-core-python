import time
from threading import Event

from adf_core_python.core.agent.action.action import Action
from adf_core_python.core.agent.agent import Agent
from adf_core_python.core.agent.config.module_config import ModuleConfig
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.info.scenario_info import Mode
from adf_core_python.core.agent.module.module_manager import ModuleManager
from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData
from adf_core_python.core.component.tactics.tactics_agent import TacticsAgent
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
        finish_post_connect_event: Event,
    ) -> None:
        super().__init__(
            is_precompute,
            self.__class__.__qualname__,
            is_debug,
            team_name,
            data_storage_name,
            module_config,
            develop_data,
            finish_post_connect_event,
        )
        self._tactics_agent = tactics_agent
        self._team_name = team_name
        self._is_precompute = is_precompute
        self._is_debug = is_debug
        self._data_storage_name = data_storage_name
        self._module_config = module_config
        self._develop_data = develop_data

    def post_connect(self) -> None:
        super().post_connect()
        self.precompute_data: PrecomputeData = PrecomputeData(self._data_storage_name)

        self._logger = get_agent_logger(
            f"{self.__class__.__module__}.{self.__class__.__qualname__}",
            self._agent_info,
        )

        self._module_manager: ModuleManager = ModuleManager(
            self._agent_info,
            self._world_info,
            self._scenario_info,
            self._module_config,
            self._develop_data,
        )

        self._message_manager.set_channel_subscriber(
            self._module_manager.get_channel_subscriber(
                "MessageManager.PlatoonChannelSubscriber",
                "adf_core_python.implement.module.communication.default_channel_subscriber.DefaultChannelSubscriber",
            )
        )
        self._message_manager.set_message_coordinator(
            self._module_manager.get_message_coordinator(
                "MessageManager.PlatoonMessageCoordinator",
                "adf_core_python.implement.module.communication.default_message_coordinator.DefaultMessageCoordinator",
            )
        )

        self._tactics_agent.initialize(
            self._agent_info,
            self._world_info,
            self._scenario_info,
            self._module_manager,
            self._precompute_data,
            self._message_manager,
            self._develop_data,
        )

        match self._scenario_info.get_mode():
            case Mode.PRECOMPUTATION:
                pass
            case Mode.PRECOMPUTED:
                pass
            case Mode.NON_PRECOMPUTE:
                start_time = time.time()
                self._logger.info(
                    f"Prepare start {self._agent_info.get_entity_id().get_value()}"
                )
                self._tactics_agent.prepare(
                    self._agent_info,
                    self._world_info,
                    self._scenario_info,
                    self._module_manager,
                    self.precompute_data,
                    self._develop_data,
                )
                self._logger.info(f"Prepare time: {time.time() - start_time:.3f} sec")

    def think(self) -> None:
        action: Action = self._tactics_agent.think(
            self._agent_info,
            self._world_info,
            self._scenario_info,
            self._module_manager,
            self._precompute_data,
            self._message_manager,
            self._develop_data,
        )
        if action is not None and self.agent_id is not None:
            self._agent_info.set_executed_action(self._agent_info.get_time(), action)
            self.send_msg(
                action.get_command(
                    self.agent_id, self._agent_info.get_time()
                ).prepare_cmd()
            )
