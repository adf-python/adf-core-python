from typing import cast

from rcrs_core.entities.fireBrigade import FireBrigadeEntity

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
from adf_core_python.core.component.tactics.tactics_fire_brigade import (
    TacticsFireBrigade,
)


class DefaultTacticsFireBrigade(TacticsFireBrigade):
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

        match scenario_info.get_mode():
            case Mode.NON_PRECOMPUTE:
                self._search: Search = cast(
                    Search,
                    module_manager.get_module(
                        "DefaultTacticsFireBrigade.Search",
                        "adf_core_python.core.component.module.complex.search.Search",
                    ),
                )
                self._human_detector: HumanDetector = cast(
                    HumanDetector,
                    module_manager.get_module(
                        "DefaultTacticsFireBrigade.HumanDetector",
                        "adf_core_python.core.component.module.complex.human_detector.HumanDetector",
                    ),
                )
                self._action_rescue = module_manager.get_extend_action(
                    "DefaultTacticsFireBrigade.ExtendActionRescue",
                    "adf_core_python.implement.action.default_extend_action_rescue.DefaultExtendActionRescue",
                )
                self._action_ext_move = module_manager.get_extend_action(
                    "DefaultTacticsAmbulanceTeam.ExtendActionMove",
                    "adf_core_python.implement.action.default_extend_action_move.DefaultExtendActionMove",
                )
        self.register_module(self._search)
        self.register_module(self._human_detector)
        self.register_action(self._action_rescue)
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

        agent: FireBrigadeEntity = cast(FireBrigadeEntity, agent_info.get_myself())  # noqa: F841
        entity_id = agent_info.get_entity_id()  # noqa: F841

        target_entity_id = self._human_detector.calculate().get_target_entity_id()
        self._logger.debug(
            f"human detector target_entity_id: {target_entity_id}",
            time=agent_info.get_time(),
        )
        if target_entity_id is not None:
            action = (
                self._action_rescue.set_target_entity_id(target_entity_id)
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
