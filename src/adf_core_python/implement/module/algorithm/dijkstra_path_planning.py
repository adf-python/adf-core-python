from __future__ import annotations

import heapq
from typing import Optional

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
    # ダイクストラ法で最短経路を計算
    queue: list[tuple[float, EntityID]] = []
    heapq.heappush(queue, (0, from_entity_id))
    distance: dict[EntityID, float] = {from_entity_id: 0}
    previous: dict[EntityID, Optional[EntityID]] = {from_entity_id: None}

    while queue:
      current_distance, current_node = heapq.heappop(queue)
      if current_node == to_entity_id:
        break

      self._logger.info(
        f"current_node: {current_node}, current_entity: {self._world_info.get_entity(current_node)}"
      )

      for neighbor, weight in self.graph[current_node]:
        new_distance = current_distance + weight
        if neighbor not in distance or new_distance < distance[neighbor]:
          distance[neighbor] = new_distance
          heapq.heappush(queue, (new_distance, neighbor))
          previous[neighbor] = current_node

    path: list[EntityID] = []
    current_path_node: Optional[EntityID] = to_entity_id
    while current_path_node is not None:
      path.append(current_path_node)
      current_path_node = previous.get(current_path_node)

    return path[::-1]

  def get_path_to_multiple_destinations(
    self, from_entity_id: EntityID, destination_entity_ids: set[EntityID]
  ) -> list[EntityID]:
    open_list = [from_entity_id]
    ancestors = {from_entity_id: from_entity_id}
    found = False
    next_node = None

    while open_list and not found:
      next_node = open_list.pop(0)
      if self.is_goal(next_node, destination_entity_ids):
        found = True
        break

      neighbors = self.graph.get(next_node, [])
      if not neighbors:
        continue

      for neighbor, _ in neighbors:
        if self.is_goal(neighbor, destination_entity_ids):
          ancestors[neighbor] = next_node
          next_node = neighbor
          found = True
          break
        elif neighbor not in ancestors:
          open_list.append(neighbor)
          ancestors[neighbor] = next_node

    if not found:
      return []

    path: list[EntityID] = []
    current = next_node
    while current != from_entity_id:
      if current is None:
        raise RuntimeError("Found a node with no ancestor! Something is broken.")
      path.insert(0, current)
      current = ancestors.get(current)
    path.insert(0, from_entity_id)

    return path

  def is_goal(self, entity_id: EntityID, target_ids: set[EntityID]) -> bool:
    return entity_id in target_ids

  def get_distance(self, from_entity_id: EntityID, to_entity_id: EntityID) -> float:
    path = self.get_path(from_entity_id, to_entity_id)
    distance = 0.0
    for i in range(len(path) - 1):
      distance += self._world_info.get_distance(path[i], path[i + 1])
    return distance
