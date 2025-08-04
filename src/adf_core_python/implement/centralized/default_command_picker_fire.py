from __future__ import annotations

from rcrscore.entities import Area, EntityID, FireBrigade, Human

from adf_core_python.core.agent.communication.standard.bundle.centralized.command_ambulance import (
  CommandAmbulance,
)
from adf_core_python.core.agent.communication.standard.bundle.centralized.command_scout import (
  CommandScout,
)
from adf_core_python.core.agent.communication.standard.bundle.standard_message_priority import (
  StandardMessagePriority,
)
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.info.agent_info import AgentInfo
from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
from adf_core_python.core.agent.info.world_info import WorldInfo
from adf_core_python.core.agent.module.module_manager import ModuleManager
from adf_core_python.core.component.centralized.command_picker import CommandPicker
from adf_core_python.core.component.communication.communication_message import (
  CommunicationMessage,
)


class DefaultCommandPickerFire(CommandPicker):
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
    self.messages: list[CommunicationMessage] = []
    self.scout_distance: int = 40000
    self.allocation_data: dict[EntityID, EntityID] = {}

  def set_allocator_result(
    self, allocation_data: dict[EntityID, EntityID]
  ) -> CommandPicker:
    self.allocation_data = allocation_data
    return self

  def calculate(self) -> CommandPicker:
    self.messages.clear()
    if not self.allocation_data:
      return self

    for ambulance_id in self.allocation_data.keys():
      agent = self._world_info.get_entity(ambulance_id)
      if agent is None or not isinstance(agent, FireBrigade):
        continue

      target = self._world_info.get_entity(self.allocation_data[ambulance_id])
      if target is None:
        continue

      command: CommunicationMessage
      if isinstance(target, Human):
        command = CommandAmbulance(
          True,
          ambulance_id,
          self._agent_info.get_entity_id(),
          CommandAmbulance.ACTION_RESCUE,
          StandardMessagePriority.NORMAL,
          target.get_entity_id(),
        )
        self.messages.append(command)

      if isinstance(target, Area):
        command = CommandScout(
          True,
          ambulance_id,
          self._agent_info.get_entity_id(),
          self.scout_distance,
          StandardMessagePriority.NORMAL,
          target.get_entity_id(),
        )
        self.messages.append(command)
    return self

  def get_result(self) -> list[CommunicationMessage]:
    return self.messages
