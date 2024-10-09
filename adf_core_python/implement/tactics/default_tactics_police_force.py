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
        self._clear_distance = int(
            scenario_info.get_value("clear.repair.distance", "null")
        )

        match scenario_info.get_mode():
            case Mode.NON_PRECOMPUTE:
                self._search: Search = cast(
                    Search,
                    module_manager.get_module(
                        "DefaultTacticsPoliceForce.Search",
                        "adf_core_python.implement.module.complex.DefaultSearch",
                    ),
                )
                self._road_detector: RoadDetector = cast(
                    RoadDetector,
                    module_manager.get_module(
                        "DefaultTacticsPoliceForce.RoadDetector",
                        "adf_core_python.implement.module.complex.DefaultRoadDetector",
                    ),
                )
                self._action_ext_clear = module_manager.get_ext_action(
                    "DefaultTacticsPoliceForce.ExtActionClear",
                    "adf_core_python.implement.extaction.DefaultExtActionClear",
                )
                self._action_ext_move = module_manager.get_ext_action(
                    "DefaultTacticsPoliceForce.ExtActionMove",
                    "adf_core_python.implement.extaction.DefaultExtActionMove",
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
        self.module_update_info(message_manager)

        agent: PoliceForceEntity = cast(PoliceForceEntity, agent_info.get_myself())  # noqa: F841
        entity_id = agent_info.get_entity_id()  # noqa: F841

        target_entity_id = self._road_detector.calculate().get_target_entity_id()
        if target_entity_id is not None:
            action = (
                self._action_ext_clear.set_target_entity_id(target_entity_id)
                .calc()
                .get_action()
            )
            if action is not None:
                return action

        target_entity_id = self._search.calculate().get_target_entity_id()
        if target_entity_id is not None:
            action = (
                self._action_ext_move.set_target_entity_id(target_entity_id)
                .calc()
                .get_action()
            )
            if action is not None:
                return action

        return ActionRest()
