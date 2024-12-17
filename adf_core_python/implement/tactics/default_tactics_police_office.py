from typing import cast

from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.communication.message_manager import MessageManager
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.info.agent_info import AgentInfo
from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
from adf_core_python.core.agent.info.world_info import WorldInfo
from adf_core_python.core.agent.module.module_manager import ModuleManager
from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData
from adf_core_python.core.component.centralized.command_picker import CommandPicker
from adf_core_python.core.component.module.complex.target_allocator import (
    TargetAllocator,
)
from adf_core_python.core.component.tactics.tactics_police_office import (
    TacticsPoliceOffice,
)


class DefaultTacticsPoliceOffice(TacticsPoliceOffice):
    def initialize(
        self,
        agent_info: AgentInfo,
        world_info: WorldInfo,
        scenario_info: ScenarioInfo,
        module_manager: ModuleManager,
        precompute_data: PrecomputeData,
        message_manager: MessageManager,
        develop_data: DevelopData,
    ) -> None:
        self._allocator: TargetAllocator = cast(
            TargetAllocator,
            module_manager.get_module(
                "DefaultTacticsPoliceOffice.TargetAllocator",
                "adf_core_python.implement.module.complex.default_police_target_allocator.DefaultPoliceTargetAllocator",
            ),
        )
        self._picker: CommandPicker = module_manager.get_command_picker(
            "DefaultTacticsPoliceOffice.CommandPicker",
            "adf_core_python.implement.centralized.default_command_picker_police.DefaultCommandPickerPolice",
        )
        self.register_module(self._allocator)
        self.register_command_picker(self._picker)

    def resume(
        self,
        agent_info: AgentInfo,
        world_info: WorldInfo,
        scenario_info: ScenarioInfo,
        module_manager: ModuleManager,
        precompute_data: PrecomputeData,
        message_manager: MessageManager,
        develop_data: DevelopData,
    ) -> None:
        self.module_resume(precompute_data)

    def precompute(
        self,
        agent_info: AgentInfo,
        world_info: WorldInfo,
        scenario_info: ScenarioInfo,
        module_manager: ModuleManager,
        precompute_data: PrecomputeData,
        message_manager: MessageManager,
        develop_data: DevelopData,
    ) -> None:
        self.module_precompute(precompute_data)

    def prepare(
        self,
        agent_info: AgentInfo,
        world_info: WorldInfo,
        scenario_info: ScenarioInfo,
        module_manager: ModuleManager,
        precompute_data: PrecomputeData,
        develop_data: DevelopData,
    ) -> None:
        self.module_prepare()

    def think(
        self,
        agent_info: AgentInfo,
        world_info: WorldInfo,
        scenario_info: ScenarioInfo,
        module_manager: ModuleManager,
        precompute_data: PrecomputeData,
        message_manager: MessageManager,
        develop_data: DevelopData,
    ) -> None:
        self.module_update_info(message_manager)

        allocation_result: dict[EntityID, EntityID] = (
            self._allocator.calculate().get_result()
        )
        for message in (
            self._picker.set_allocator_result(allocation_result)
            .calculate()
            .get_result()
        ):
            message_manager.add_message(message)
