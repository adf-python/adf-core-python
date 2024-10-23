from typing import Optional, Union, cast

from rcrs_core.entities.ambulanceTeam import AmbulanceTeamEntity
from rcrs_core.entities.area import Area
from rcrs_core.entities.civilian import Civilian
from rcrs_core.entities.entity import Entity
from rcrs_core.entities.human import Human
from rcrs_core.entities.refuge import Refuge
from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.action.ambulance.action_load import ActionLoad
from adf_core_python.core.agent.action.ambulance.action_unload import ActionUnload
from adf_core_python.core.agent.action.common.action_move import ActionMove
from adf_core_python.core.agent.action.common.action_rest import ActionRest
from adf_core_python.core.agent.communication.message_manager import MessageManager
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.info.agent_info import AgentInfo
from adf_core_python.core.agent.info.scenario_info import Mode, ScenarioInfo
from adf_core_python.core.agent.info.world_info import WorldInfo
from adf_core_python.core.agent.module.module_manager import ModuleManager
from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData
from adf_core_python.core.component.action.extend_action import ExtendAction
from adf_core_python.core.component.module.algorithm.path_planning import PathPlanning
from adf_core_python.core.logger.logger import get_agent_logger


# TODO: refactor this class
class DefaultExtendActionTransport(ExtendAction):
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
        self._target_entity_id: Optional[EntityID] = None
        self._threshold_to_rest: int = develop_data.get_value("threshold_to_rest", 100)
        self._logger = get_agent_logger(
            f"{self.__class__.__module__}.{self.__class__.__qualname__}",
            self.agent_info,
        )

        match self.scenario_info.get_mode():
            case Mode.NON_PRECOMPUTE:
                self._path_planning: PathPlanning = cast(
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
        if self.get_count_precompute() > 1:
            return self
        self._path_planning.precompute(precompute_data)
        return self

    def resume(self, precompute_data: PrecomputeData) -> ExtendAction:
        super().resume(precompute_data)
        if self.get_count_resume() > 1:
            return self
        self._path_planning.resume(precompute_data)
        return self

    def prepare(self) -> ExtendAction:
        super().prepare()
        if self.get_count_prepare() > 1:
            return self
        self._path_planning.prepare()
        return self

    def update_info(self, message_manager: MessageManager) -> ExtendAction:
        super().update_info(message_manager)
        if self.get_count_update_info() > 1:
            return self
        self._path_planning.update_info(message_manager)
        return self

    def set_target_entity_id(self, target_entity_id: EntityID) -> ExtendAction:
        entity: Optional[Entity] = self.world_info.get_world_model().get_entity(
            target_entity_id
        )
        self._target_entity_id = None

        if entity is None:
            return self

        if isinstance(entity, Human) or isinstance(entity, Area):
            self._target_entity_id = target_entity_id

        return self

    def calculate(self) -> ExtendAction:
        self._result = None
        agent: AmbulanceTeamEntity = cast(
            AmbulanceTeamEntity, self.agent_info.get_myself()
        )
        transport_human: Optional[Human] = self.agent_info.some_one_on_board()
        if transport_human is not None:
            self._logger.debug(f"transport_human: {transport_human.get_id()}")
            self.result = self.calc_unload(
                agent, self._path_planning, transport_human, self._target_entity_id
            )
            if self.result is not None:
                return self

        if self._target_entity_id is not None:
            self.result = self.calc_rescue(
                agent, self._path_planning, self._target_entity_id
            )

        return self

    def calc_rescue(
        self,
        agent: AmbulanceTeamEntity,
        path_planning: PathPlanning,
        target_id: EntityID,
    ) -> Optional[Union[ActionMove, ActionLoad]]:
        target_entity = self.world_info.get_entity(target_id)
        if target_entity is None:
            return None

        agent_position = agent.get_position()
        if isinstance(target_entity, Human):
            human = target_entity
            if human.get_position() is None:
                return None
            if human.get_hp() is None or human.get_hp() == 0:
                return None

            target_position = human.get_position()
            if agent_position == target_position:
                if isinstance(human, Civilian) and ((human.get_buriedness() or 0) == 0):
                    return ActionLoad(human.get_id())
            else:
                path = path_planning.get_path(agent_position, target_position)
                if path is not None and len(path) > 0:
                    return ActionMove(path)
            return None

        if isinstance(target_entity, Area):
            path = path_planning.get_path(agent_position, target_entity.get_id())
            if path is not None and len(path) > 0:
                return ActionMove(path)

        return None

    def calc_unload(
        self,
        agent: AmbulanceTeamEntity,
        path_planning: PathPlanning,
        transport_human: Optional[Human],
        target_id: Optional[EntityID],
    ) -> Optional[ActionMove | ActionUnload | ActionRest]:
        if transport_human is None:
            return None

        if not transport_human.get_hp() or transport_human.get_hp() == 0:
            return ActionUnload()

        agent_position = agent.get_position()
        if (
            target_id is None
            or transport_human.get_id().get_value() == target_id.get_value()
        ):
            position = self.world_info.get_entity(agent_position)
            if position is None:
                return None

            if isinstance(position, Refuge):
                return ActionUnload()
            else:
                path = self.get_nearest_refuge_path(agent, path_planning)
                if path is not None and len(path) > 0:
                    return ActionMove(path)

        if target_id is None:
            return None

        target_entity = self.world_info.get_entity(target_id)

        if isinstance(target_entity, Human):
            human = cast(Human, target_entity)
            if human.get_position() is not None:
                return self.calc_refuge_action(
                    agent, path_planning, human.get_position(), True
                )
            path = self.get_nearest_refuge_path(agent, path_planning)
            if path is not None and len(path) > 0:
                return ActionMove(path)

        return None

    def calc_refuge_action(
        self,
        human: Human,
        path_planning: PathPlanning,
        target_entity_id: EntityID,
        is_unload: bool,
    ) -> Optional[ActionMove | ActionUnload | ActionRest]:
        position = human.get_position()
        refuges = self.world_info.get_entity_ids_of_types([Refuge])
        size = len(refuges)

        if position in refuges:
            return ActionUnload() if is_unload else ActionRest()

        first_result = None
        while len(refuges) > 0:
            path = path_planning.get_path(position, refuges[0])

            if path is not None and len(path) > 0:
                if first_result is None:
                    first_result = path.copy()

                refuge_id = path[-1]
                from_refuge_to_target = path_planning.get_path(
                    refuge_id, target_entity_id
                )

                if from_refuge_to_target is not None and len(from_refuge_to_target) > 0:
                    return ActionMove(path)

                refuges.remove(refuge_id)
                if size == len(refuges):
                    break
                size = len(refuges)
            else:
                break

        return ActionMove(first_result) if first_result is not None else None

    def get_nearest_refuge_path(
        self, human: Human, path_planning: PathPlanning
    ) -> list[EntityID]:
        position = human.get_position()
        refuges = self.world_info.get_entity_ids_of_types([Refuge])
        nearest_path = None

        for refuge_id in refuges:
            path: list[EntityID] = path_planning.get_path(position, refuge_id)
            if len(path) > 0:
                if nearest_path is None or len(path) < len(nearest_path):
                    nearest_path = path

        return nearest_path if nearest_path is not None else []
