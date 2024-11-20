from typing import Optional, cast

from rcrs_core.connection.URN import Entity as EntityURN
from rcrs_core.entities.civilian import Civilian
from rcrs_core.entities.entity import Entity
from rcrs_core.entities.human import Human
from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.info.agent_info import AgentInfo
from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
from adf_core_python.core.agent.info.world_info import WorldInfo
from adf_core_python.core.agent.module.module_manager import ModuleManager
from adf_core_python.core.component.module.algorithm.clustering import Clustering
from adf_core_python.core.component.module.complex.human_detector import HumanDetector
from adf_core_python.core.logger.logger import get_agent_logger


class SampleHumanDetector(HumanDetector):
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
        self._clustering: Clustering = cast(
            Clustering,
            module_manager.get_module(
                "DefaultHumanDetector.Clustering",
                "adf_core_python.implement.module.algorithm.k_means_clustering.KMeansClustering",
            ),
        )
        self.register_sub_module(self._clustering)

        self._result: Optional[EntityID] = None
        self._logger = get_agent_logger(
            f"{self.__class__.__module__}.{self.__class__.__qualname__}",
            self._agent_info,
        )

    def calculate(self) -> HumanDetector:
        transport_human: Optional[Human] = self._agent_info.some_one_on_board()
        if transport_human is not None:
            self._result = transport_human.get_id()
            return self

        if self._result is not None:
            if not self._is_valid_human(self._result):
                self._result = None

        if self._result is None:
            self._result = self._select_target()

        return self

    def _select_target(self) -> Optional[EntityID]:
        if self._result is not None and self._is_valid_human(self._result):
            return self._result

        cluster_index: int = self._clustering.get_cluster_index(
            self._agent_info.get_entity_id()
        )
        cluster_entities: list[Entity] = self._clustering.get_cluster_entities(
            cluster_index
        )

        cluster_valid_human_entities: list[Entity] = [
            entity
            for entity in cluster_entities
            if self._is_valid_human(entity.get_id()) and isinstance(entity, Civilian)
        ]
        if len(cluster_valid_human_entities) != 0:
            nearest_human_entity = cluster_valid_human_entities[0]
            nearest_distance = self._world_info.get_distance(
                self._agent_info.get_entity_id(),
                nearest_human_entity.get_id(),
            )
            for entity in cluster_valid_human_entities:
                distance = self._world_info.get_distance(
                    self._agent_info.get_entity_id(),
                    entity.get_id(),
                )
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_human_entity = entity
            return nearest_human_entity.get_id()

        world_valid_human_entities: list[Entity] = [
            entity
            for entity in self._world_info.get_entities_of_types([Civilian])
            if self._is_valid_human(entity.get_id())
        ]
        if len(world_valid_human_entities) != 0:
            nearest_human_entity = world_valid_human_entities[0]
            nearest_distance = self._world_info.get_distance(
                self._agent_info.get_entity_id(),
                nearest_human_entity.get_id(),
            )
            for entity in world_valid_human_entities:
                distance = self._world_info.get_distance(
                    self._agent_info.get_entity_id(),
                    entity.get_id(),
                )
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_human_entity = entity
            return nearest_human_entity.get_id()

        return None

    def _is_valid_human(self, target_entity_id: EntityID) -> bool:
        target: Optional[Entity] = self._world_info.get_entity(target_entity_id)
        if target is None:
            return False
        if not isinstance(target, Human):
            return False
        hp: Optional[int] = target.get_hp()
        if hp is None or hp <= 0:
            return False
        buriedness: Optional[int] = target.get_buriedness()
        if buriedness is None:
            return False
        myself = self._agent_info.get_myself()
        if myself.get_urn() == EntityURN.FIRE_BRIGADE and buriedness == 0:
            return False
        if myself.get_urn() == EntityURN.AMBULANCE_TEAM and buriedness > 0:
            return False
        damage: Optional[int] = target.get_damage()
        if damage is None or damage == 0:
            return False
        position_entity_id: Optional[EntityID] = target.get_position()
        if position_entity_id is None:
            return False
        position: Optional[Entity] = self._world_info.get_entity(position_entity_id)
        if position is None:
            return False
        urn: EntityURN = position.get_urn()
        if urn == EntityURN.REFUGE or urn == EntityURN.AMBULANCE_TEAM:
            return False

        return True

    def get_target_entity_id(self) -> Optional[EntityID]:
        return self._result
