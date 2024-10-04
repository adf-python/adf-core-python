from logging import Logger, getLogger
from typing import Optional, cast

from rcrs_core.entities.area import Area
from rcrs_core.entities.blockade import Blockade
from rcrs_core.entities.entity import Entity
from rcrs_core.entities.human import Human
from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.action.common.action_move import ActionMove
from adf_core_python.core.agent.communication.message_manager import MessageManager
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.info.agent_info import AgentInfo
from adf_core_python.core.agent.info.scenario_info import Mode, ScenarioInfo
from adf_core_python.core.agent.info.world_info import WorldInfo
from adf_core_python.core.agent.module.module_manager import ModuleManager
from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData
from adf_core_python.core.component.extaction.ext_action import ExtAction
from adf_core_python.core.component.module.algorithm.path_planning import PathPlanning


class DefaultExtendActionMove(ExtAction):
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
        self._logger: Logger = getLogger(__name__)

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

    def precompute(self, precompute_data: PrecomputeData) -> ExtAction:
        super().precompute(precompute_data)
        if self.get_count_precompute() > 1:
            return self
        self._path_planning.precompute(precompute_data)
        return self

    def resume(self, precompute_data: PrecomputeData) -> ExtAction:
        super().resume(precompute_data)
        if self.get_count_resume() > 1:
            return self
        self._path_planning.resume(precompute_data)
        return self

    def prepare(self) -> ExtAction:
        super().prepare()
        if self.get_count_prepare() > 1:
            return self
        self._path_planning.prepare()
        return self

    def update_info(self, message_manager: MessageManager) -> ExtAction:
        super().update_info(message_manager)
        if self.get_count_update_info() > 1:
            return self
        self._path_planning.update_info(message_manager)
        return self

    def set_target_entity_id(self, target_entity_id: EntityID) -> ExtAction:
        entity: Optional[Entity] = self.world_info.get_entity(target_entity_id)
        self._target_entity_id = None

        if entity is None:
            return self

        if isinstance(entity, Blockade):
            entity = self.world_info.get_entity(cast(Blockade, entity).get_position())
        elif isinstance(entity, Human):
            entity = entity.get_position()

        if entity is not None and isinstance(entity, Area):
            self._target_entity_id = entity.get_id()

        return self

    def calc(self) -> ExtAction:
        self.result = None
        agent: Human = cast(Human, self.agent_info.get_myself())

        path: list[EntityID] = self._path_planning.get_path(
            agent.get_position(), self._target_entity_id
        )

        if path is not None and len(path) != 0:
            self.result = ActionMove(path)

        return self
