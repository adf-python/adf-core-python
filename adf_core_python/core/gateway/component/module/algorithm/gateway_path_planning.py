from __future__ import annotations

import json
from typing import TYPE_CHECKING

from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.component.module.algorithm.path_planning import PathPlanning
from adf_core_python.core.gateway.component.module.gateway_abstract_module import (
    GatewayAbstractModule,
)

if TYPE_CHECKING:
    from adf_core_python.core.agent.communication.message_manager import MessageManager
    from adf_core_python.core.agent.develop.develop_data import DevelopData
    from adf_core_python.core.agent.info.agent_info import AgentInfo
    from adf_core_python.core.agent.info.world_info import WorldInfo
    from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
    from adf_core_python.core.agent.module.module_manager import ModuleManager
    from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData
    from adf_core_python.core.gateway.gateway_module import GatewayModule


class GatewayPathPlanning(GatewayAbstractModule, PathPlanning):
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

    def precompute(self, precompute_data: PrecomputeData) -> GatewayPathPlanning:
        super().precompute(precompute_data)
        return self

    def resume(self, precompute_data: PrecomputeData) -> GatewayPathPlanning:
        super().resume(precompute_data)
        return self

    def prepare(self) -> GatewayPathPlanning:
        super().prepare()
        return self

    def update_info(self, message_manager: MessageManager) -> GatewayPathPlanning:
        super().update_info(message_manager)
        return self

    def calculate(self) -> GatewayPathPlanning:
        super().calculate()
        return self

    def get_path(
        self, from_entity_id: EntityID, to_entity_id: EntityID
    ) -> list[EntityID]:
        arguments: dict[str, str] = {
            "From": str(from_entity_id.get_value()),
            "To": str(to_entity_id.get_value()),
        }
        result = self._gateway_module.execute(
            "getResult(EntityID, EntityID)", arguments
        )
        json_str = result.get_value_or_default("Result", "[]")
        raw_entity_ids: list[int] = json.loads(json_str)
        entity_ids: list[EntityID] = []
        for entity_id in raw_entity_ids:
            entity_ids.append(EntityID(entity_id))
        return entity_ids

    def get_distance(self, from_entity_id: EntityID, to_entity_id: EntityID) -> float:
        arguments: dict[str, str] = {
            "From": str(from_entity_id.get_value()),
            "To": str(to_entity_id.get_value()),
        }
        result = self._gateway_module.execute(
            "getDistance(EntityID, EntityID)", arguments
        )
        return float(result.get_value_or_default("Result", "0.0"))
