from __future__ import annotations

from abc import abstractmethod

from rcrs_core.entities.area import Area

from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData
from adf_core_python.core.component.module.complex.target_detector import TargetDetector


class Search(TargetDetector[Area]):
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

    def precompute(self, precompute_data: PrecomputeData) -> Search:
        super().precompute(precompute_data)
        return self

    def resume(self, precompute_data: PrecomputeData) -> Search:
        super().resume(precompute_data)
        return self

    def prepare(self) -> Search:
        super().prepare()
        return self

    @abstractmethod
    def calculate(self) -> Search:
        return self
