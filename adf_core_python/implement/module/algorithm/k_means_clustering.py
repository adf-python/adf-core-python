import numpy as np
from rcrs_core.connection.URN import Entity as EntityURN
from rcrs_core.entities.ambulanceCenter import AmbulanceCentre
from rcrs_core.entities.building import Building
from rcrs_core.entities.entity import Entity
from rcrs_core.entities.fireStation import FireStation
from rcrs_core.entities.gasStation import GasStation
from rcrs_core.entities.hydrant import Hydrant
from rcrs_core.entities.policeOffice import PoliceOffice
from rcrs_core.entities.refuge import Refuge
from rcrs_core.entities.road import Road
from rcrs_core.worldmodel.entityID import EntityID
from sklearn.cluster import KMeans

from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.info.agent_info import AgentInfo
from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
from adf_core_python.core.agent.info.world_info import WorldInfo
from adf_core_python.core.agent.module.module_manager import ModuleManager
from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData
from adf_core_python.core.component.module.algorithm.clustering import Clustering


class KMeansClustering(Clustering):
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
        match agent_info.get_myself().get_urn():
            case EntityURN.AMBULANCE_TEAM:
                self._cluster_number = int(
                    scenario_info.get_value(
                        "scenario.agents.at",
                        1,
                    )
                )
            case EntityURN.POLICE_FORCE:
                self._cluster_number = int(
                    scenario_info.get_value(
                        "scenario.agents.pf",
                        1,
                    )
                )
            case EntityURN.FIRE_BRIGADE:
                self._cluster_number = int(
                    scenario_info.get_value(
                        "scenario.agents.fb",
                        1,
                    )
                )
            case _:
                self._cluster_number = 1

        sorted_entities = sorted(
            world_info.get_entities_of_types(
                [
                    agent_info.get_myself().__class__,
                ]
            ),
            key=lambda entity: entity.get_id().get_value(),
        )
        self.entity_cluster_indices = {
            entity.get_id(): idx for idx, entity in enumerate(sorted_entities)
        }

        self.cluster_entities: list[list[Entity]] = []
        self.entities: list[Entity] = world_info.get_entities_of_types(
            [
                AmbulanceCentre,
                FireStation,
                GasStation,
                Hydrant,
                PoliceOffice,
                Refuge,
                Road,
                Building,
            ]
        )

    def calculate(self) -> Clustering:
        return self

    def precompute(self, precompute_data: PrecomputeData) -> Clustering:
        cluster_entities = self.create_cluster(self._cluster_number, self.entities)
        precompute_data.write_json_data(
            {
                "cluster_entities": [
                    [entity.get_id().get_value() for entity in cluster]
                    for cluster in cluster_entities
                ]
            },
            self.__class__.__name__,
        )
        return self

    def resume(self, precompute_data: PrecomputeData) -> Clustering:
        data = precompute_data.read_json_data(self.__class__.__name__)
        self.cluster_entities = [
            [
                entity
                for entity_id in cluster
                if (entity := self._world_info.get_entity(EntityID(entity_id)))
                is not None
            ]
            for cluster in data["cluster_entities"]
        ]
        return self

    def get_cluster_number(self) -> int:
        return self._cluster_number

    def get_cluster_index(self, entity_id: EntityID) -> int:
        return self.entity_cluster_indices.get(entity_id, 0)

    def get_cluster_entities(self, cluster_index: int) -> list[Entity]:
        if cluster_index >= len(self.cluster_entities):
            return []
        return self.cluster_entities[cluster_index]

    def get_cluster_entity_ids(self, cluster_index: int) -> list[EntityID]:
        if cluster_index >= len(self.cluster_entities):
            return []
        return [entity.get_id() for entity in self.cluster_entities[cluster_index]]

    def prepare(self) -> Clustering:
        super().prepare()
        if self.get_count_prepare() > 1:
            return self
        self.cluster_entities = self.create_cluster(self._cluster_number, self.entities)
        return self

    def create_cluster(
        self, cluster_number: int, entities: list[Entity]
    ) -> list[list[Entity]]:
        kmeans = KMeans(n_clusters=cluster_number, random_state=0)
        entity_positions: np.ndarray = np.array([])
        for entity in entities:
            location1_x, location1_y = entity.get_location()
            if location1_x is None or location1_y is None:
                continue
            entity_positions = np.append(entity_positions, [location1_x, location1_y])

        kmeans.fit(entity_positions.reshape(-1, 2))

        clusters: list[list[Entity]] = [[] for _ in range(cluster_number)]
        for entity, label in zip(entities, kmeans.labels_):
            clusters[label].append(entity)

        return clusters
