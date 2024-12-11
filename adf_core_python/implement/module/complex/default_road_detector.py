from typing import Optional, cast

from rcrs_core.entities.building import Building
from rcrs_core.entities.gasStation import GasStation
from rcrs_core.entities.refuge import Refuge
from rcrs_core.entities.road import Road
from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.communication.message_manager import MessageManager
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.info.agent_info import AgentInfo
from adf_core_python.core.agent.info.scenario_info import Mode, ScenarioInfo
from adf_core_python.core.agent.info.world_info import WorldInfo
from adf_core_python.core.agent.module.module_manager import ModuleManager
from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData
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

        self._path_planning: PathPlanning = cast(
            PathPlanning,
            module_manager.get_module(
                "DefaultRoadDetector.PathPlanning",
                "adf_core_python.implement.module.algorithm.a_star_path_planning.AStarPathPlanning",
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

        self._target_areas: set[EntityID] = set()
        entities = self._world_info.get_entities_of_types(
            [Refuge, Building, GasStation]
        )
        for entity in entities:
            if not isinstance(entity, Building):
                continue
            for entity_id in entity.get_neighbours():
                neighbor = self._world_info.get_entity(entity_id)
                if isinstance(neighbor, Road):
                    self._target_areas.add(entity_id)

        self._priority_roads = set()
        for entity in self._world_info.get_entities_of_types([Refuge]):
            if not isinstance(entity, Building):
                continue
            for entity_id in entity.get_neighbours():
                neighbor = self._world_info.get_entity(entity_id)
                if isinstance(neighbor, Road):
                    self._priority_roads.add(entity_id)

        return self

    def prepare(self) -> RoadDetector:
        super().prepare()
        if self.get_count_prepare() >= 2:
            return self

        self._target_areas = set()
        entities = self._world_info.get_entities_of_types(
            [Refuge, Building, GasStation]
        )
        for entity in entities:
            building: Building = cast(Building, entity)
            for entity_id in building.get_neighbours():
                neighbor = self._world_info.get_entity(entity_id)
                if isinstance(neighbor, Road):
                    self._target_areas.add(entity_id)

        self._priority_roads = set()
        for entity in self._world_info.get_entities_of_types([Refuge]):
            refuge: Refuge = cast(Refuge, entity)
            for entity_id in refuge.get_neighbours():
                neighbor = self._world_info.get_entity(entity_id)
                if isinstance(neighbor, Road):
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

    def calculate(self) -> RoadDetector:
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
                _nearest_target_area = self._agent_info.get_position_entity_id()
                _nearest_distance = float("inf")
                for target_area in self._target_areas:
                    if (
                        self._world_info.get_distance(
                            self._agent_info.get_position_entity_id(), target_area
                        )
                        < _nearest_distance
                    ):
                        _nearest_target_area = target_area
                        _nearest_distance = self._world_info.get_distance(
                            self._agent_info.get_position_entity_id(), target_area
                        )
                path: list[EntityID] = self._path_planning.get_path(
                    self._agent_info.get_position_entity_id(), _nearest_target_area
                )
                if path is not None and len(path) > 0:
                    self._result = path[-1]

        return self

    def get_target_entity_id(self) -> Optional[EntityID]:
        return self._result
