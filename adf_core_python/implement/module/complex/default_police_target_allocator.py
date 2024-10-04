from functools import cmp_to_key

from rcrs_core.entities.policeForce import PoliceForceEntity
from rcrs_core.worldmodel.entityID import EntityID
from rcrs_core.entities.refuge import Refuge
from rcrs_core.entities.building import Building
from rcrs_core.entities.gassStation import GasStation
from rcrs_core.entities.road import Road

from adf_core_python.core.component.module.complex.police_target_allocator import (
    PoliceTargetAllocator,
)


class DefaultPoliceTargetAllocator(PoliceTargetAllocator):
    def __init__(
        self,
        agent_info,
        world_info,
        scenario_info,
        module_manager,
        develop_data,
    ):
        super().__init__(
            agent_info, world_info, scenario_info, module_manager, develop_data
        )
        self._priority_areas = set()
        self._target_areas = set()
        self._agent_info_map = {}

    def resume(self, precompute_data):
        super().resume(precompute_data)
        if self.get_count_resume() >= 2:
            return self

        for entity_id in self._world_info.get_entity_ids_of_type(PoliceForceEntity):
            self._agent_info_map[entity_id] = self.PoliceForceInfo(entity_id)
            for entity in (
                self._world_info.get_entities_of_type(Refuge)
                + self._world_info.get_entities_of_type(Building)
                + self._world_info.get_entities_of_type(GasStation)
            ):
                for entity_id in entity.get_neighbours():
                    neighbour = self._world_info.get_entity(entity_id)
                    if isinstance(neighbour, Road):
                        self._target_areas.add(entity_id)

            for entity in self._world_info.get_entities_of_type(Refuge):
                for entity_id in entity.get_neighbours():
                    neighbour = self._world_info.get_entity(entity_id)
                    if isinstance(neighbour, Road):
                        self._priority_areas.add(entity_id)
        return self

    def prepare(self):
        super().prepare()
        if self.get_count_prepare() >= 2:
            return self

        for entity_id in self._world_info.get_entity_ids_of_type(PoliceForceEntity):
            self._agent_info_map[entity_id] = self.PoliceForceInfo(entity_id)

        for entity in (
            self._world_info.get_entities_of_type(Refuge)
            + self._world_info.get_entities_of_type(Building)
            + self._world_info.get_entities_of_type(GasStation)
        ):
            for entity_id in entity.get_neighbours():
                neighbour = self._world_info.get_entity(entity_id)
                if isinstance(neighbour, Road):
                    self._target_areas.add(entity_id)

        for entity in self._world_info.get_entities_of_type(Refuge):
            for entity_id in entity.get_neighbours():
                neighbour = self._world_info.get_entity(entity_id)
                if isinstance(neighbour, Road):
                    self._priority_areas.add(entity_id)

        return self

    def update_info(self, message_manager):
        super().update_info(message_manager)
        # TODO: implement after message_manager is implemented
        return self

    def calculate(self):
        agents = self.get_action_agents(self._agent_info_map)
        removes = []
        current_time = self._agent_info.get_time()

        for target in self._priority_areas:
            if len(agents) > 0:
                target_entity = self._world_info.get_entity(target)
                if target_entity is not None:
                    agents = sorted(
                        agents, key=cmp_to_key(self._compare_by_distance(target_entity))
                    )
                    result = agents.pop(0)
                    info = self._agent_info_map[result.get_id()]
                    if info is not None:
                        info._can_new_action = False
                        info._target = target
                        info.command_time = current_time
                        self._agent_info_map[result.get_id()] = info
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
                result = areas.pop(0)
                self._target_areas.remove(result.get_id())
                info = self._agent_info_map[agent.get_id()]
                if info is not None:
                    info._can_new_action = False
                    info._target = result.get_id()
                    info.command_time = current_time
                    self._agent_info_map[agent.get_id()] = info

        return self

    def get_result(self):
        return self._convert(self._agent_info_map)

    def _compare_by_distance(self, target_entity):
        def _cmp_func(self, entity_a, entity_b):
            distance_a = self._world_info.get_distance(target_entity, entity_a)
            distance_b = self._world_info.get_distance(target_entity, entity_b)
            if distance_a < distance_b:
                return -1
            elif distance_a > distance_b:
                return 1
            else:
                return 0

    def _convert(self, info_map):
        result = {}
        for entity_id in info_map.keys():
            info = info_map[entity_id]
            if info is not None and info._target is not None:
                result[entity_id] = info._target

    class PoliceForceInfo:
        def __init__(self, entity_id: EntityID):
            self._agent_id = entity_id
            self._target = None
            self._can_new_action = True
            self.command_time = -1
