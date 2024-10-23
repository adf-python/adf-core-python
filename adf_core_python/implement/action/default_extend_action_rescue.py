from typing import cast, Optional

from rcrs_core.entities.area import Area
from rcrs_core.entities.blockade import Blockade
from rcrs_core.entities.fireBrigade import FireBrigadeEntity
from rcrs_core.entities.human import Human
from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.action.action import Action
from adf_core_python.core.agent.action.ambulance.action_rescue import ActionRescue
from adf_core_python.core.agent.action.common.action_move import ActionMove
from adf_core_python.core.agent.communication.message_manager import MessageManager
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.info.agent_info import AgentInfo
from adf_core_python.core.agent.info.scenario_info import ScenarioInfo, Mode
from adf_core_python.core.agent.info.world_info import WorldInfo
from adf_core_python.core.agent.module.module_manager import ModuleManager
from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData
from adf_core_python.core.component.action.extend_action import ExtendAction
from adf_core_python.core.component.module.algorithm.path_planning import PathPlanning


class DefaultExtendActionRescue(ExtendAction):
    def __init__(
        self,
        agent_info: AgentInfo,
        world_info: WorldInfo,
        scenario_info: ScenarioInfo,
        module_manager: ModuleManager,
        develop_data: DevelopData,
    ) -> None:
        super().__init__(
            agent_info, world_info, scenario_info, module_manager, develop_data
        )
        self._kernel_time = None
        self._target_entity_id = None
        self._threshold_rest = develop_data.get_value(
            "adf_core_python.implement.action.DefaultExtendActionRescue.rest", 100
        )

        match self.scenario_info.get_mode():
            case Mode.NON_PRECOMPUTE:
                self._path_planning = cast(
                    PathPlanning,
                    self.module_manager.get_module(
                        "DefaultExtendActionMove.PathPlanning",
                        "adf_core_python.implement.module.algorithm.a_star_path_planning.AStarPathPlanning",
                    ),
                )
            case Mode.PRECOMPUTATION:
                pass
            case Mode.PRECOMPUTED:
                pass

    def precompute(self, precompute_data: PrecomputeData) -> ExtendAction:
        super().precompute(precompute_data)
        if self.get_count_precompute() >= 2:
            return self
        self._path_planning.precompute(precompute_data)
        self._kernel_time = self.scenario_info.get_value("kernel.timesteps", -1)
        return self

    def resume(self, precompute_data: PrecomputeData) -> ExtendAction:
        super().resume(precompute_data)
        if self.get_count_resume() >= 2:
            return self
        self._path_planning.resume(precompute_data)
        self._kernel_time = self.scenario_info.get_value("kernel.timesteps", -1)
        return self

    def prepare(self) -> ExtendAction:
        super().prepare()
        if self.get_count_prepare() >= 2:
            return self
        self._path_planning.prepare()
        self._kernel_time = self.scenario_info.get_value("kernel.timesteps", -1)
        return self

    def update_info(self, message_manager: MessageManager) -> ExtendAction:
        super().update_info(message_manager)
        if self.get_count_update_info() >= 2:
            return self
        self._path_planning.update_info(message_manager)
        return self

    def set_target_entity_id(self, target_entity_id: EntityID) -> ExtendAction:
        self._target_entity_id = None
        if target_entity_id is not None:
            entity = self.world_info.get_entity(target_entity_id)
            if isinstance(entity, Human) or isinstance(entity, Area):
                self._target_entity_id = target_entity_id
                return self
        return self

    def calculate(self) -> ExtendAction:
        self.result = None
        agent = cast(FireBrigadeEntity, self.agent_info.get_myself())

        if self._target_entity_id is not None:
            self.result = self._calc_rescue(
                agent, self._path_planning, self._target_entity_id
            )

        return self

    def _calc_rescue(
        self,
        agent: FireBrigadeEntity,
        path_planning: PathPlanning,
        target_entity_id: EntityID,
    ) -> Optional[Action]:
        target_entity = self.world_info.get_entity(target_entity_id)
        if target_entity is None:
            return None

        agent_position_entity_id = agent.get_position()
        if isinstance(target_entity, Human):
            human = cast(Human, target_entity)
            if human.get_hp() == 0:
                return None

            target_position_entity_id = human.get_position()
            if (
                agent_position_entity_id.get_value()
                == target_position_entity_id.get_value()
            ):
                buriedness = human.get_buriedness()
                if buriedness is not None and buriedness > 0:
                    return ActionRescue(target_entity_id)
            else:
                path = path_planning.get_path(
                    agent_position_entity_id, target_position_entity_id
                )
                if path != []:
                    return ActionMove(path)

            return None

        if isinstance(target_entity, Blockade):
            blockade = cast(Blockade, target_entity)
            target_entity = self.world_info.get_entity(blockade.get_position())
            if isinstance(target_entity, Area):
                path = self._path_planning.get_path(
                    agent_position_entity_id, target_entity.get_id()
                )
                if path != []:
                    return ActionMove(path)

        return None
