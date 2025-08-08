from functools import cmp_to_key
from typing import Callable, Optional, cast

from rcrscore.entities import (
  Building,
  Entity,
  EntityID,
  GasStation,
  PoliceForce,
  Refuge,
  Road,
)

from adf_core_python.core.agent.communication.message_manager import MessageManager
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.info.agent_info import AgentInfo
from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
from adf_core_python.core.agent.info.world_info import WorldInfo
from adf_core_python.core.agent.module.module_manager import ModuleManager
from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData
from adf_core_python.core.component.module.complex.police_target_allocator import (
  PoliceTargetAllocator,
)


class DefaultPoliceTargetAllocator(PoliceTargetAllocator):
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
    self._priority_areas: set[EntityID] = set()
    self._target_areas: set[EntityID] = set()
    self._agent_info_map: dict[
      EntityID, DefaultPoliceTargetAllocator.PoliceForceInfo
    ] = {}

  def resume(self, precompute_data: PrecomputeData) -> PoliceTargetAllocator:
    super().resume(precompute_data)
    if self.get_count_resume() >= 2:
      return self

    for entity_id in self._world_info.get_entity_ids_of_types([PoliceForce]):
      self._agent_info_map[entity_id] = self.PoliceForceInfo(entity_id)
      for entity in self._world_info.get_entities_of_types(
        [Refuge, Building, GasStation]
      ):
        building: Building = cast(Building, entity)
        for entity_id in building.get_neighbors():
          neighbor = self._world_info.get_entity(entity_id)
          if isinstance(neighbor, Road):
            self._target_areas.add(entity_id)

      for entity in self._world_info.get_entities_of_types([Refuge]):
        refuge: Refuge = cast(Refuge, entity)
        for entity_id in refuge.get_neighbors():
          neighbor = self._world_info.get_entity(entity_id)
          if isinstance(neighbor, Road):
            self._priority_areas.add(entity_id)
    return self

  def prepare(self) -> PoliceTargetAllocator:
    super().prepare()
    if self.get_count_prepare() >= 2:
      return self

    for entity_id in self._world_info.get_entity_ids_of_types([PoliceForce]):
      self._agent_info_map[entity_id] = self.PoliceForceInfo(entity_id)

    for entity in self._world_info.get_entities_of_types(
      [Refuge, Building, GasStation]
    ):
      building: Building = cast(Building, entity)
      for entity_id in building.get_neighbors():
        neighbor = self._world_info.get_entity(entity_id)
        if isinstance(neighbor, Road):
          self._target_areas.add(entity_id)

    for entity in self._world_info.get_entities_of_types([Refuge]):
      refuge: Refuge = cast(Refuge, entity)
      for entity_id in refuge.get_neighbors():
        neighbor = self._world_info.get_entity(entity_id)
        if isinstance(neighbor, Road):
          self._priority_areas.add(entity_id)

    return self

  def update_info(self, message_manager: MessageManager) -> PoliceTargetAllocator:
    super().update_info(message_manager)
    # TODO: implement after message_manager is implemented
    return self

  def calculate(self) -> PoliceTargetAllocator:
    agents = self._get_action_agents(self._agent_info_map)
    removes = []
    current_time = self._agent_info.get_time()

    for target in self._priority_areas:
      if len(agents) > 0:
        target_entity = self._world_info.get_entity(target)
        if target_entity is not None:
          agents = sorted(
            agents, key=cmp_to_key(self._compare_by_distance(target_entity))
          )
          selected_agent = agents.pop(0)
          info = self._agent_info_map[selected_agent.get_entity_id()]
          if info is not None:
            info._can_new_action = False
            info._target = target
            info.command_time = current_time
            self._agent_info_map[selected_agent.get_entity_id()] = info
            removes.append(target)

    for r in removes:
      self._priority_areas.remove(r)

    areas = []
    for target in self._target_areas:
      target_entity = self._world_info.get_entity(target)
      if target_entity is not None:
        areas.append(target_entity)

    for agent in agents:
      if len(areas) > 0:
        areas.sort(key=cmp_to_key(self._compare_by_distance(agent)))
        target_area: Entity = areas.pop(0)
        self._target_areas.remove(target_area.get_entity_id())
        info = self._agent_info_map[agent.get_entity_id()]
        if info is not None:
          info._can_new_action = False
          info._target = target_area.get_entity_id()
          info.command_time = current_time
          self._agent_info_map[agent.get_entity_id()] = info

    return self

  def get_result(self) -> dict[EntityID, EntityID]:
    return self._convert(self._agent_info_map)

  def _get_action_agents(
    self, info_map: dict[EntityID, "DefaultPoliceTargetAllocator.PoliceForceInfo"]
  ) -> list[PoliceForce]:
    result = []
    for entity in self._world_info.get_entities_of_types([PoliceForce]):
      if isinstance(entity, PoliceForce):
        info = info_map[entity.get_entity_id()]
        if info is not None and info._can_new_action:
          result.append(entity)
    return result

  def _compare_by_distance(
    self, target_entity: Entity
  ) -> Callable[[Entity, Entity], int]:
    def _cmp_func(entity_a: Entity, entity_b: Entity) -> int:
      distance_a = self._world_info.get_distance(
        target_entity.get_entity_id(), entity_a.get_entity_id()
      )
      distance_b = self._world_info.get_distance(
        target_entity.get_entity_id(), entity_b.get_entity_id()
      )
      if distance_a < distance_b:
        return -1
      elif distance_a > distance_b:
        return 1
      else:
        return 0

    return _cmp_func

  def _convert(
    self, info_map: dict[EntityID, "DefaultPoliceTargetAllocator.PoliceForceInfo"]
  ) -> dict[EntityID, EntityID]:
    result: dict[EntityID, EntityID] = {}
    for entity_id in info_map.keys():
      info = info_map[entity_id]
      if info is not None and info._target is not None:
        result[entity_id] = info._target
    return result

  class PoliceForceInfo:
    def __init__(self, entity_id: EntityID) -> None:
      self._agent_id: EntityID = entity_id
      self._target: Optional[EntityID] = None
      self._can_new_action: bool = True
      self.command_time: int = -1
