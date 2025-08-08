from __future__ import annotations

import json
from typing import TYPE_CHECKING

from rcrscore.entities import EntityID

from adf_core_python.core.component.module.algorithm.clustering import Clustering
from adf_core_python.core.gateway.component.module.gateway_abstract_module import (
  GatewayAbstractModule,
)

if TYPE_CHECKING:
  from rcrscore.entities.entity import Entity

  from adf_core_python.core.agent.communication.message_manager import MessageManager
  from adf_core_python.core.agent.develop.develop_data import DevelopData
  from adf_core_python.core.agent.info.agent_info import AgentInfo
  from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
  from adf_core_python.core.agent.info.world_info import WorldInfo
  from adf_core_python.core.agent.module.module_manager import ModuleManager
  from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData
  from adf_core_python.core.gateway.gateway_module import GatewayModule


class GatewayClustering(GatewayAbstractModule, Clustering):
  def __init__(
    self,
    agent_info: AgentInfo,
    world_info: WorldInfo,
    scenario_info: ScenarioInfo,
    module_manager: ModuleManager,
    develop_data: DevelopData,
    gateway_module: GatewayModule,
  ) -> None:
    super().__init__(
      agent_info,
      world_info,
      scenario_info,
      module_manager,
      develop_data,
      gateway_module,
    )

  def precompute(self, precompute_data: PrecomputeData) -> GatewayClustering:
    super().precompute(precompute_data)
    return self

  def resume(self, precompute_data: PrecomputeData) -> GatewayClustering:
    super().resume(precompute_data)
    return self

  def prepare(self) -> GatewayClustering:
    super().prepare()
    return self

  def update_info(self, message_manager: MessageManager) -> GatewayClustering:
    super().update_info(message_manager)
    return self

  def calculate(self) -> GatewayClustering:
    super().calculate()
    return self

  def get_cluster_number(self) -> int:
    result = self._gateway_module.execute("getClusterNumber")
    return int(result.get_value("ClusterNumber") or 0)

  def get_cluster_index(self, entity_id: EntityID) -> int:
    arguments: dict[str, str] = {"EntityID": str(entity_id.get_value())}
    result = self._gateway_module.execute("getClusterIndex(EntityID)", arguments)
    return int(result.get_value("ClusterIndex") or 0)

  def get_cluster_entities(self, cluster_index: int) -> list[Entity]:
    arguments: dict[str, str] = {"Index": str(cluster_index)}
    result = self._gateway_module.execute("getClusterEntities(int)", arguments)
    json_str = result.get_value("EntityIDs") or "[]"
    entity_ids: list[int] = json.loads(json_str)
    entities: list[Entity] = []
    for entity_id in entity_ids:
      entity = self._world_info.get_entity(EntityID(entity_id))
      if entity is not None:
        entities.append(entity)
    return entities

  def get_cluster_entity_ids(self, cluster_index: int) -> list[EntityID]:
    arguments: dict[str, str] = {"Index": str(cluster_index)}
    result = self._gateway_module.execute("getClusterEntityIDs(int)", arguments)
    json_str = result.get_value("EntityIDs") or "[]"
    raw_entity_ids: list[int] = json.loads(json_str)
    entity_ids: list[EntityID] = []
    for entity_id in raw_entity_ids:
      entity_ids.append(EntityID(entity_id))
    return entity_ids
