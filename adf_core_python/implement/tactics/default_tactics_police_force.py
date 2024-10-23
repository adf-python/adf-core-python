from typing import cast

from rcrs_core.entities.policeForce import PoliceForceEntity

from adf_core_python.core.agent.action.action import Action
from adf_core_python.core.agent.action.common.action_rest import ActionRest
from adf_core_python.core.agent.communication.message_manager import MessageManager
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.info.agent_info import AgentInfo
from adf_core_python.core.agent.info.scenario_info import Mode, ScenarioInfo
from adf_core_python.core.agent.info.world_info import WorldInfo
from adf_core_python.core.agent.module.module_manager import ModuleManager
from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData
from adf_core_python.core.component.module.complex.road_detector import RoadDetector
from adf_core_python.core.component.module.complex.search import Search
from adf_core_python.core.component.tactics.tactics_police_force import (
    TacticsPoliceForce,
)


class DefaultTacticsPoliceForce(TacticsPoliceForce):
    def initialize(
        self,
        agent_info: AgentInfo,
        world_info: WorldInfo,
        scenario_info: ScenarioInfo,
        module_manager: ModuleManager,
        precompute_data: PrecomputeData,
        message_manager: MessageManager,
        develop_data: DevelopData,
    ) -> None:
        # world_info.index_class()
        super().initialize(
            agent_info,
            world_info,
            scenario_info,
            module_manager,
            precompute_data,
            message_manager,
            develop_data,
        )
        # self._clear_distance = int(
        #     scenario_info.get_value("clear.repair.distance", "null")
        # )

        match scenario_info.get_mode():
            case Mode.NON_PRECOMPUTE:
                self._search: Search = cast(
                    Search,
                    module_manager.get_module(
                        "DefaultTacticsPoliceForce.Search",
                        "adf_core_python.core.component.module.complex.search.Search",
                    ),
                )
                self._road_detector: RoadDetector = cast(
                    RoadDetector,
                    module_manager.get_module(
                        "DefaultTacticsPoliceForce.RoadDetector",
                        "adf_core_python.core.component.module.complex.road_detector.RoadDetector",
                    ),
                )
                self._action_ext_clear = module_manager.get_extend_action(
                    "DefaultTacticsPoliceForce.ExtendActionClear",
                    "adf_core_python.implement.action.default_extend_action_clear.DefaultExtendActionClear",
                )
                self._action_ext_move = module_manager.get_extend_action(
                    "DefaultTacticsPoliceForce.ExtendActionMove",
                    "adf_core_python.implement.action.default_extend_action_move.DefaultExtendActionMove",
                )
        self.register_module(self._search)
        self.register_module(self._road_detector)
        self.register_action(self._action_ext_clear)
        self.register_action(self._action_ext_move)

    def precompute(
        self,
        agent_info: AgentInfo,
        world_info: WorldInfo,
        scenario_info: ScenarioInfo,
        module_manager: ModuleManager,
        precompute_data: PrecomputeData,
        message_manager: MessageManager,
        develop_data: DevelopData,
    ) -> None:
        self.module_precompute(precompute_data)

    def resume(
        self,
        agent_info: AgentInfo,
        world_info: WorldInfo,
        scenario_info: ScenarioInfo,
        module_manager: ModuleManager,
        precompute_data: PrecomputeData,
        message_manager: MessageManager,
        develop_data: DevelopData,
    ) -> None:
        self.module_resume(precompute_data)

    def prepare(
        self,
        agent_info: AgentInfo,
        world_info: WorldInfo,
        scenario_info: ScenarioInfo,
        module_manager: ModuleManager,
        precompute_data: PrecomputeData,
        develop_data: DevelopData,
    ) -> None:
        self.module_prepare()

    def think(
        self,
        agent_info: AgentInfo,
        world_info: WorldInfo,
        scenario_info: ScenarioInfo,
        module_manager: ModuleManager,
        precompute_data: PrecomputeData,
        message_manager: MessageManager,
        develop_data: DevelopData,
    ) -> Action:
        self.reset_count()
        self.module_update_info(message_manager)

        agent: PoliceForceEntity = cast(PoliceForceEntity, agent_info.get_myself())  # noqa: F841
        entity_id = agent_info.get_entity_id()  # noqa: F841

        target_entity_id = self._road_detector.calculate().get_target_entity_id()
        self._logger.debug(
            f"road detector target_entity_id: {target_entity_id}",
            time=agent_info.get_time(),
        )
        if target_entity_id is not None:
            action = (
                self._action_ext_clear.set_target_entity_id(target_entity_id)
                .calculate()
                .get_action()
            )
            if action is not None:
                self._logger.debug(f"action: {action}", time=agent_info.get_time())
                return action

        target_entity_id = self._search.calculate().get_target_entity_id()
        self._logger.debug(
            f"search target_entity_id: {target_entity_id}", time=agent_info.get_time()
        )
        if target_entity_id is not None:
            action = (
                self._action_ext_move.set_target_entity_id(target_entity_id)
                .calculate()
                .get_action()
            )
            if action is not None:
                self._logger.debug(f"action: {action}", time=agent_info.get_time())
                return action

        return ActionRest()
