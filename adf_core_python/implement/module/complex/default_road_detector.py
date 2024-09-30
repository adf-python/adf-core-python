from __future__ import annotations

from typing import TYPE_CHECKING, cast

from rcrs_core.entities.refuge import Refuge
from rcrs_core.entities.building import Building
from rcrs_core.entities.gassStation import GasStation
from rcrs_core.entities.road import Road
from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.communication.message_manager import MessageManager
from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData
from adf_core_python.core.component.module.complex.road_detector import RoadDetector
from adf_core_python.core.component.module.complex.target_detector import TargetDetector

if TYPE_CHECKING:
    from adf_core_python.core.agent.develop.develop_data import DevelopData
    from adf_core_python.core.agent.info.agent_info import AgentInfo
    from adf_core_python.core.agent.info.scenario_info import Mode, ScenarioInfo
    from adf_core_python.core.agent.info.world_info import WorldInfo
    from adf_core_python.core.agent.module.module_manager import ModuleManager
    from adf_core_python.core.component.module.algorithm.path_planning import (
        PathPlanning,
    )
    from adf_core_python.core.component.module.complex.road_detector import RoadDetector


class DefaultRoadDetector(RoadDetector):
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
        match scenario_info.get_mode():
            case Mode.NON_PRECOMPUTE:
                self._path_planning: PathPlanning = cast(
                    PathPlanning,
                    self.module_manager.get_module(
                        "DefaultRoadDetector.PathPlanning",
                        "adf_core_python.implement.module.algorithm.DijkstraPathPlanning",
                    ),
                )

        self.register_sub_module(self._path_planning)
        self._result = None

    def precompute(self, precompute_data: PrecomputeData) -> RoadDetector:
        super().precompute(precompute_data)
        return self

    def resume(self, precompute_data: PrecomputeData) -> RoadDetector:
        super().resume(precompute_data)
        if self.get_count_resume() >= 2:
            return self

        self._target_areas = set()
        entities = (
            self._world_info.get_entities_of_type(Refuge)
            + self._world_info.get_entities_of_type(Building)
            + self._world_info.get_entities_of_type(GasStation)
        )
        for entity in entities:
            if not isinstance(entity, Building):
                continue
            for entity_id in entity.get_neighbours():
                neighbour = self._world_info.get_entity(entity_id)
                if isinstance(neighbour, Road):
                    self._target_areas.add(entity_id)

        self._priority_roads = set()
        for entity in self._world_info.get_entities_of_type(Refuge):
            if not isinstance(entity, Building):
                continue
            for entity_id in entity.get_neighbours():
                if isinstance(neighbour, Road):
                    self._priority_roads.add(entity_id)

        return self

    def prepare(self) -> RoadDetector:
        super().prepare()
        if self.get_count_prepare() >= 2:
            return self

        self._target_areas = set()
        entities = (
            self._world_info.get_entities_of_type(Refuge)
            + self._world_info.get_entities_of_type(Building)
            + self._world_info.get_entities_of_type(GasStation)
        )
        for entity in entities:
            building: Building = cast(Building, entity)
            for entity_id in building.get_neighbours():
                neighbour = self._world_info.get_entity(entity_id)
                if isinstance(neighbour, Road):
                    self._target_areas.add(entity_id)

        self._priority_roads = set()
        for entity in self._world_info.get_entities_of_type(Refuge):
            refuge: Refuge = cast(Refuge, entity)
            for entity_id in refuge.get_neighbours():
                if isinstance(neighbour, Road):
                    self._priority_roads.add(entity_id)

        return self

    def update_info(self, message_manager: MessageManager) -> RoadDetector:
        super().update_info(message_manager)
        if self.get_count_update_info() >= 2:
            return self

        if self._result is not None:
            if self._agent_info.get_position_entity_id == self._result:
                entity = self._world_info.get_entity(self._result)
                if isinstance(entity, Building):
                    self._result = None
                elif isinstance(entity, Road):
                    road: Road = cast(Road, entity)
                    if road.get_blockades() == []:
                        self._target_areas.remove(self._result)
                        self._result = None

        return self

    def calc(self) -> RoadDetector:
        if self._result is None:
            position_entity_id: EntityID = self._agent_info.get_position_entity_id()
            if position_entity_id in self._target_areas:
                self._result = position_entity_id
                return self
            remove_list = []
            for entity_id in self._priority_roads:
                if entity_id not in self._target_areas:
                    remove_list.append(entity_id)

            self._priority_roads = self._priority_roads - set(remove_list)
            if len(self._priority_roads) > 0:
                self._path_planning.set_from(position_entity_id)
                self._path_planning.set_destination(list(self._target_areas))
                path: list[EntityID] = self._path_planning.calculate().get_path()
                if path is not None and len(path) > 0:
                    self._result = path[-1]

        return self

    def get_target(self) -> EntityID:
        return self._result
