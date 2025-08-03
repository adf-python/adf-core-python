from functools import cmp_to_key
from typing import Callable, Optional

from rcrscore.entities import Entity, EntityID, FireBrigade, Human

from adf_core_python.core.agent.communication.message_manager import MessageManager
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.info.agent_info import AgentInfo
from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
from adf_core_python.core.agent.info.world_info import WorldInfo
from adf_core_python.core.agent.module.module_manager import ModuleManager
from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData
from adf_core_python.core.component.module.complex.fire_target_allocator import (
    FireTargetAllocator,
)


class DefaultFireTargetAllocator(FireTargetAllocator):
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
        self._priority_humans: set[EntityID] = set()
        self._target_humans: set[EntityID] = set()
        self._fire_brigade_info_map: dict[
            EntityID, DefaultFireTargetAllocator.FireBrigadeInfo
        ] = {}

    def resume(self, precompute_data: PrecomputeData) -> FireTargetAllocator:
        super().resume(precompute_data)
        if self.get_count_resume() >= 2:
            return self
        for entity_id in self._world_info.get_entity_ids_of_types([FireBrigade]):
            self._fire_brigade_info_map[entity_id] = self.FireBrigadeInfo(entity_id)
        return self

    def prepare(self) -> FireTargetAllocator:
        super().prepare()
        if self.get_count_prepare() >= 2:
            return self
        for entity_id in self._world_info.get_entity_ids_of_types([FireBrigade]):
            self._fire_brigade_info_map[entity_id] = self.FireBrigadeInfo(entity_id)
        return self

    def update_info(self, message_manager: MessageManager) -> FireTargetAllocator:
        super().update_info(message_manager)
        # TODO: implement after message_manager is implemented
        return self

    def calculate(self) -> FireTargetAllocator:
        agents = self._get_action_agents(self._fire_brigade_info_map)
        removes = []
        current_time = self._agent_info.get_time()

        for target in self._priority_humans:
            if len(agents) > 0:
                target_entity = self._world_info.get_entity(target)
                if target_entity is not None and isinstance(target_entity, Human):
                    agents = sorted(
                        agents, key=cmp_to_key(self._compare_by_distance(target_entity))
                    )
                    result = agents.pop(0)
                    info = self._fire_brigade_info_map[result.get_entity_id()]
                    if info is not None:
                        info._can_new_action = False
                        info._target = target
                        info.command_time = current_time
                        self._fire_brigade_info_map[result.get_entity_id()] = info
                        removes.append(target)

        for r in removes:
            self._priority_humans.remove(r)
        removes.clear()

        for target in self._target_humans:
            if len(agents) > 0:
                target_entity = self._world_info.get_entity(target)
                if target_entity is not None and isinstance(target_entity, Human):
                    agents = sorted(
                        agents, key=cmp_to_key(self._compare_by_distance(target_entity))
                    )
                    result = agents.pop(0)
                    info = self._fire_brigade_info_map[result.get_entity_id()]
                    if info is not None:
                        info._can_new_action = False
                        info._target = target
                        info.command_time = current_time
                        self._fire_brigade_info_map[result.get_entity_id()] = info
                        removes.append(target)

        for r in removes:
            self._target_humans.remove(r)

        return self

    def get_result(self) -> dict[EntityID, EntityID]:
        return self._convert(self._fire_brigade_info_map)

    def _get_action_agents(
        self, info_map: dict[EntityID, "DefaultFireTargetAllocator.FireBrigadeInfo"]
    ) -> list[FireBrigade]:
        result = []
        for entity in self._world_info.get_entities_of_types([FireBrigade]):
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
        self, info_map: dict[EntityID, "DefaultFireTargetAllocator.FireBrigadeInfo"]
    ) -> dict[EntityID, EntityID]:
        result = {}
        for entity_id in info_map.keys():
            info = info_map[entity_id]
            if info is not None and info._target is not None:
                result[entity_id] = info._target
        return result

    class FireBrigadeInfo:
        def __init__(self, entity_id: EntityID) -> None:
            self._agent_id: EntityID = entity_id
            self._target: Optional[EntityID] = None
            self._can_new_action: bool = True
            self.command_time: int = -1
