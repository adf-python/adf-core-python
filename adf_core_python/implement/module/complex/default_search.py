from typing import Optional, cast

from rcrs_core.entities.building import Building
from rcrs_core.entities.entity import Entity
from rcrs_core.entities.refuge import Refuge
from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.communication.message_manager import MessageManager
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.info.agent_info import AgentInfo
from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
from adf_core_python.core.agent.info.world_info import WorldInfo
from adf_core_python.core.agent.module.module_manager import ModuleManager
from adf_core_python.core.component.module.algorithm.clustering import Clustering
from adf_core_python.core.component.module.algorithm.path_planning import PathPlanning
from adf_core_python.core.component.module.complex.search import Search


class DefaultSearch(Search):
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

        self._unsearched_building_ids: set[EntityID] = set()
        self._result: Optional[EntityID] = None

        self._clustering: Clustering = cast(
            Clustering,
            module_manager.get_module(
                "DefaultSearch.Clustering",
                "adf_core_python.implement.module.algorithm.k_means_clustering.KMeansClustering",
            ),
        )

        self._path_planning: PathPlanning = cast(
            PathPlanning,
            module_manager.get_module(
                "DefaultSearch.PathPlanning",
                "adf_core_python.implement.module.algorithm.a_star_path_planning.AStarPathPlanning",
            ),
        )

        self.register_sub_module(self._clustering)
        self.register_sub_module(self._path_planning)

    def update_info(self, message_manager: MessageManager) -> Search:
        super().update_info(message_manager)
        if self.get_count_update_info() > 1:
            return self

        searched_building_id = self._agent_info.get_position_entity_id()
        self._unsearched_building_ids.discard(searched_building_id)

        if len(self._unsearched_building_ids) == 0:
            self._unsearched_building_ids = self._get_search_targets()

        return self

    def calculate(self) -> Search:
        nearest_building_id: Optional[EntityID] = None
        nearest_distance: Optional[float] = None
        for building_id in self._unsearched_building_ids:
            distance = self._world_info.get_distance(
                self._agent_info.get_entity_id(), building_id
            )
            if nearest_distance is None or distance < nearest_distance:
                nearest_building_id = building_id
                nearest_distance = distance
        self._result = nearest_building_id
        return self

    def get_target_entity_id(self) -> Optional[EntityID]:
        return self._result

    def _get_search_targets(self) -> set[EntityID]:
        cluster_index: int = self._clustering.get_cluster_index(
            self._agent_info.get_entity_id()
        )
        cluster_entities: list[Entity] = self._clustering.get_cluster_entities(
            cluster_index
        )
        building_entity_ids: list[EntityID] = [
            entity.get_id()
            for entity in cluster_entities
            if isinstance(entity, Building) and not isinstance(entity, Refuge)
        ]

        return set(building_entity_ids)
