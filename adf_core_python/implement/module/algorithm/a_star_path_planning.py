from __future__ import annotations

from rcrs_core.entities.area import Area
from rcrs_core.entities.entity import Entity
from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.info.agent_info import AgentInfo
from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
from adf_core_python.core.agent.info.world_info import WorldInfo
from adf_core_python.core.agent.module.module_manager import ModuleManager
from adf_core_python.core.component.module.algorithm.path_planning import (
    PathPlanning,
)


class AStarPathPlanning(PathPlanning):
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
        entities: list[Entity] = self._world_info.get_entities_of_types([Area])
        self._graph: dict[EntityID, set[EntityID]] = {}
        for entity in entities:
            if isinstance(entity, Area):
                self._graph[entity.get_id()] = set(
                    neighbor
                    for neighbor in entity.get_neighbours()  # TODO: Fix rcrs_core typo
                    if neighbor != EntityID(0)
                )

    def get_path(
        self, from_entity_id: EntityID, to_entity_id: EntityID
    ) -> list[EntityID]:
        open_set: set[EntityID] = {from_entity_id}
        came_from: dict[EntityID, EntityID] = {}
        g_score: dict[EntityID, float] = {from_entity_id: 0.0}
        f_score: dict[EntityID, float] = {
            from_entity_id: self.heuristic(from_entity_id, to_entity_id)
        }

        while open_set:
            current: EntityID = min(
                open_set, key=lambda x: f_score.get(x, float("inf"))
            )
            if current == to_entity_id:
                return self.reconstruct_path(came_from, current)

            open_set.remove(current)
            for neighbor in self._graph.get(current, []):
                tentative_g_score: float = g_score[current] + self.distance(
                    current, neighbor
                )
                if tentative_g_score < g_score.get(neighbor, float("inf")):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(
                        neighbor, to_entity_id
                    )
                    if neighbor not in open_set:
                        open_set.add(neighbor)

        return []

    def get_path_to_multiple_destinations(
        self, from_entity_id: EntityID, destination_entity_ids: set[EntityID]
    ) -> list[EntityID]:
        return []

    def heuristic(self, from_entity_id: EntityID, to_entity_id: EntityID) -> float:
        # Implement a heuristic function, for example, Euclidean distance
        return self._world_info.get_distance(from_entity_id, to_entity_id)

    def distance(self, from_entity_id: EntityID, to_entity_id: EntityID) -> float:
        # Implement a distance function, for example, Euclidean distance
        return self._world_info.get_distance(from_entity_id, to_entity_id)

    def reconstruct_path(
        self, came_from: dict[EntityID, EntityID], current: EntityID
    ) -> list[EntityID]:
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        total_path.reverse()
        return total_path

    def get_distance(self, from_entity_id: EntityID, to_entity_id: EntityID) -> float:
        path: list[EntityID] = self.get_path(from_entity_id, to_entity_id)
        distance: float = 0.0
        for i in range(len(path) - 1):
            distance += self.distance(path[i], path[i + 1])
        return distance

    def calculate(self) -> AStarPathPlanning:
        return self
