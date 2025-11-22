from typing import TYPE_CHECKING, cast

from adf_core_python.core.agent.communication import MessageManager
from adf_core_python.core.agent.develop import DevelopData
from adf_core_python.core.agent.info import AgentInfo, ScenarioInfo, WorldInfo
from adf_core_python.core.agent.module import ModuleManager
from adf_core_python.core.agent.precompute import PrecomputeData
from adf_core_python.core.component.tactics import (
  TacticsAmbulanceCenter,
)

if TYPE_CHECKING:
  from rcrscore.entities import EntityID

  from adf_core_python.core.component.centralized import CommandPicker
  from adf_core_python.core.component.module.complex import (
    TargetAllocator,
  )


class DefaultTacticsAmbulanceCenter(TacticsAmbulanceCenter):
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
      "TargetAllocator",
      module_manager.get_module(
        "DefaultTacticsAmbulanceCenter.TargetAllocator",
        "adf_core_python.implement.module.complex.default_ambulance_target_allocator.DefaultAmbulanceTargetAllocator",
      ),
    )
    self._picker: CommandPicker = module_manager.get_command_picker(
      "DefaultTacticsAmbulanceCenter.CommandPicker",
      "adf_core_python.implement.centralized.default_command_picker_ambulance.DefaultCommandPickerAmbulance",
    )
    self.register_module(self._allocator)
    self.register_command_picker(self._picker)

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
      self._picker.set_allocator_result(allocation_result).calculate().get_result()
    ):
      message_manager.add_message(message)
