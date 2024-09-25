from typing import cast

from rcrs_core.entities.ambulanceTeam import AmbulanceTeamEntity

from adf_core_python.core.agent.action.action import Action
from adf_core_python.core.agent.action.common.action_rest import ActionRest
from adf_core_python.core.agent.communication.message_manager import MessageManager
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.info.agent_info import AgentInfo
from adf_core_python.core.agent.info.scenario_info import Mode, ScenarioInfo
from adf_core_python.core.agent.info.world_info import WorldInfo
from adf_core_python.core.agent.module.module_manager import ModuleManager
from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData
from adf_core_python.core.component.module.complex.human_detector import HumanDetector
from adf_core_python.core.component.module.complex.search import Search
from adf_core_python.core.component.tactics.tactics_ambulance_team import (
    TacticsAmbulanceTeam,
)


class DefaultTacticsAmbulanceTeam(TacticsAmbulanceTeam):
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
        match scenario_info.get_mode():
            case Mode.NON_PRECOMPUTE:
                self._search: Search = cast(
                    Search,
                    module_manager.get_module(
                        "DefaultTacticsAmbulanceTeam.Search",
                        "adf.impl.module.complex.DefaultSearch",
                    ),
                )
                self._human_detector: HumanDetector = cast(
                    HumanDetector,
                    module_manager.get_module(
                        "DefaultTacticsAmbulanceTeam.HumanDetector",
                        "adf.impl.module.complex.DefaultHumanDetector",
                    ),
                )
                self._actionTransport = module_manager.get_ext_action(
                    "DefaultTacticsAmbulanceTeam.ExtActionMove",
                    "adf.impl.extaction.DefaultExtActionMove",
                )
                self._actionExtMove = module_manager.get_ext_action(
                    "DefaultTacticsAmbulanceTeam.ExtActionMove",
                    "adf.impl.extaction.DefaultExtActionMove",
                )
                self.register_module(self._search)
                self.register_module(self._human_detector)
                self.register_action(self._actionTransport)
                self.register_action(self._actionExtMove)

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

        agent: AmbulanceTeamEntity = cast(AmbulanceTeamEntity, agent_info.get_myself())  # noqa: F841
        entity_id = agent_info.get_entity_id()  # noqa: F841

        target_entity_id = self._human_detector.calculate().get_target_entity_id()
        action = (
            self._actionTransport.set_target_entity_id(target_entity_id)
            .calc()
            .get_action()
        )
        if action is not None:
            return action

        target_entity_id = self._search.calculate().get_target_entity_id()
        action = (
            self._actionExtMove.set_target_entity_id(target_entity_id)
            .calc()
            .get_action()
        )
        if action is not None:
            return action

        return ActionRest()