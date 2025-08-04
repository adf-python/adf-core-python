from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from rcrscore.entities.road import Road

from adf_core_python.core.component.module.complex.target_detector import (
    TargetDetector,
)

if TYPE_CHECKING:
    from adf_core_python.core.agent.develop.develop_data import DevelopData
    from adf_core_python.core.agent.info.agent_info import AgentInfo
    from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
    from adf_core_python.core.agent.info.world_info import WorldInfo
    from adf_core_python.core.agent.module.module_manager import ModuleManager
    from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData


class RoadDetector(TargetDetector[Road]):
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

    def precompute(self, precompute_data: PrecomputeData) -> RoadDetector:
        super().precompute(precompute_data)
        return self

    def resume(self, precompute_data: PrecomputeData) -> RoadDetector:
        super().resume(precompute_data)
        return self

    def prepare(self) -> RoadDetector:
        super().prepare()
        return self

    @abstractmethod
    def calculate(self) -> RoadDetector:
        return self
