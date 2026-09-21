from __future__ import annotations

import heapq
from itertools import count
from typing import Callable

from rcrscore.entities import Area, Building, EntityID, Road

from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.info.agent_info import AgentInfo
from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
from adf_core_python.core.agent.info.world_info import WorldInfo
from adf_core_python.core.agent.module.module_manager import ModuleManager
from adf_core_python.core.component.module.algorithm.path_planning import PathPlanning


class DijkstraPathPlanning(PathPlanning):
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
    self.graph: dict[EntityID, list[tuple[EntityID, float]]] = {}
    # グラフの構築
    for area in self._world_info.get_entities_of_types([Road, Building]):
      if not isinstance(area, Area):
        continue
      if (neighbors := area.get_neighbors()) is None:
        continue
      area_id = area.get_entity_id()
      self.graph[area_id] = [
        (
          neighbor,
          self._world_info.get_distance(area_id, entity_id2=neighbor),
        )
        for neighbor in neighbors
        if neighbor.get_value() != 0
      ]

  def calculate(self) -> PathPlanning:
    return self

  def get_path(
    self, from_entity_id: EntityID, to_entity_id: EntityID
  ) -> list[EntityID]:
    path, _ = self._shortest_path(from_entity_id, lambda node: node == to_entity_id)
    return path

  def get_path_to_multiple_destinations(
    self, from_entity_id: EntityID, destination_entity_ids: set[EntityID]
  ) -> list[EntityID]:
    path, _ = self._shortest_path(
      from_entity_id, lambda node: node in destination_entity_ids
    )
    return path

  def is_goal(self, entity_id: EntityID, target_ids: set[EntityID]) -> bool:
    return entity_id in target_ids

  def get_distance(self, from_entity_id: EntityID, to_entity_id: EntityID) -> float:
    _, distance = self._shortest_path(from_entity_id, lambda node: node == to_entity_id)
    return distance

  def _shortest_path(
    self, source: EntityID, is_target: Callable[[EntityID], bool]
  ) -> tuple[list[EntityID], float]:
    if source not in self.graph:
      return [], float("inf")

    sequence = count()
    queue: list[tuple[float, int, EntityID]] = [(0.0, next(sequence), source)]
    distances = {source: 0.0}
    previous: dict[EntityID, EntityID] = {}

    while queue:
      current_distance, _, current = heapq.heappop(queue)
      if current_distance > distances[current]:
        continue
      if is_target(current):
        path = [current]
        while current in previous:
          current = previous[current]
          path.append(current)
        path.reverse()
        return path, current_distance

      for neighbor, weight in self.graph.get(current, []):
        if neighbor not in self.graph:
          continue
        new_distance = current_distance + weight
        if new_distance < distances.get(neighbor, float("inf")):
          distances[neighbor] = new_distance
          previous[neighbor] = current
          heapq.heappush(queue, (new_distance, next(sequence), neighbor))

    return [], float("inf")
