from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from adf_core_python.core.component.module.abstract_module import AbstractModule

if TYPE_CHECKING:
    from rcrs_core.entities.entity import Entity
    from rcrs_core.worldmodel.entityID import EntityID

    from adf_core_python.core.agent.communication.message_manager import MessageManager
    from adf_core_python.core.agent.develop.develop_data import DevelopData
    from adf_core_python.core.agent.info.agent_info import AgentInfo
    from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
    from adf_core_python.core.agent.info.world_info import WorldInfo
    from adf_core_python.core.agent.module.module_manager import ModuleManager
    from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData


class Clustering(AbstractModule):
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

    @abstractmethod
    def get_cluster_number(self) -> int:
        pass

    @abstractmethod
    def get_cluster_index(self, entity_id: EntityID) -> int:
        pass

    @abstractmethod
    def get_cluster_entities(self, cluster_index: int) -> list[Entity]:
        pass

    @abstractmethod
    def get_cluster_entity_ids(self, cluster_index: int) -> list[EntityID]:
        pass

    @abstractmethod
    def calculate(self) -> Clustering:
        pass

    def precompute(self, precompute_data: PrecomputeData) -> Clustering:
        super().precompute(precompute_data)
        return self

    def resume(self, precompute_data: PrecomputeData) -> Clustering:
        super().resume(precompute_data)
        return self

    def prepare(self) -> Clustering:
        super().prepare()
        return self

    def update_info(self, message_manager: MessageManager) -> Clustering:
        super().update_info(message_manager)
        return self
