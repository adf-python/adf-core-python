from typing import Optional

from rcrscore.urn import EntityURN

from adf_core_python.core.agent.communication import MessageManager
from adf_core_python.core.agent.communication.standard.bundle import (
  StandardMessage,
  StandardMessagePriority,
)
from adf_core_python.core.agent.communication.standard.bundle.centralized import (
  CommandAmbulance,
  CommandFire,
  CommandPolice,
  CommandScout,
  MessageReport,
)
from adf_core_python.core.agent.communication.standard.bundle.information import (
  MessageAmbulanceTeam,
  MessageBuilding,
  MessageCivilian,
  MessageFireBrigade,
  MessagePoliceForce,
  MessageRoad,
)
from adf_core_python.core.agent.info import (
  AgentInfo,
  ScenarioInfo,
  ScenarioInfoKeys,
  WorldInfo,
)
from adf_core_python.core.component.communication import (
  CommunicationMessage,
  MessageCoordinator,
)
from adf_core_python.implement.module.communication.default_channel_subscriber import (
  DefaultChannelSubscriber,
)


class DefaultMessageCoordinator(MessageCoordinator):
  def coordinate(
    self,
    agent_info: AgentInfo,
    world_info: WorldInfo,
    scenario_info: ScenarioInfo,
    message_manager: MessageManager,
    send_message_list: list[CommunicationMessage],
    channel_send_message_list: list[list[CommunicationMessage]],
  ) -> None:
    police_messages: list[StandardMessage] = []
    ambulance_messages: list[StandardMessage] = []
    fire_brigade_messages: list[StandardMessage] = []
    voice_messages: list[StandardMessage] = []

    agent_type = self.get_agent_type(agent_info, world_info)

    for msg in send_message_list:
      if isinstance(msg, StandardMessage) and not msg.is_wireless_message():
        voice_messages.append(msg)
      else:
        if isinstance(msg, MessageBuilding):
          fire_brigade_messages.append(msg)
        elif isinstance(msg, MessageCivilian):
          ambulance_messages.append(msg)
        elif isinstance(msg, MessageRoad):
          fire_brigade_messages.append(msg)
          ambulance_messages.append(msg)
          police_messages.append(msg)
        elif isinstance(msg, CommandAmbulance):
          ambulance_messages.append(msg)
        elif isinstance(msg, CommandFire):
          fire_brigade_messages.append(msg)
        elif isinstance(msg, CommandPolice):
          police_messages.append(msg)
        elif isinstance(msg, CommandScout):
          if agent_type == EntityURN.FIRE_STATION:
            fire_brigade_messages.append(msg)
          elif agent_type == EntityURN.POLICE_OFFICE:
            police_messages.append(msg)
          elif agent_type == EntityURN.AMBULANCE_CENTER:
            ambulance_messages.append(msg)
        elif isinstance(msg, MessageReport):
          if agent_type == EntityURN.FIRE_BRIGADE:
            fire_brigade_messages.append(msg)
          elif agent_type == EntityURN.POLICE_FORCE:
            police_messages.append(msg)
          elif agent_type == EntityURN.AMBULANCE_TEAM:
            ambulance_messages.append(msg)
        elif isinstance(msg, MessageFireBrigade):
          fire_brigade_messages.append(msg)
          ambulance_messages.append(msg)
          police_messages.append(msg)
        elif isinstance(msg, MessagePoliceForce):
          ambulance_messages.append(msg)
          police_messages.append(msg)
        elif isinstance(msg, MessageAmbulanceTeam):
          ambulance_messages.append(msg)
          police_messages.append(msg)

    if int(scenario_info.get_value("comms.channels.count", 1)) > 1:
      channel_size = [0] * (int(scenario_info.get_value("comms.channels.count", 1)))
      self.set_send_messages(
        scenario_info,
        EntityURN.POLICE_FORCE,
        agent_info,
        world_info,
        police_messages,
        channel_send_message_list,
        channel_size,
      )
      self.set_send_messages(
        scenario_info,
        EntityURN.AMBULANCE_TEAM,
        agent_info,
        world_info,
        ambulance_messages,
        channel_send_message_list,
        channel_size,
      )
      self.set_send_messages(
        scenario_info,
        EntityURN.FIRE_BRIGADE,
        agent_info,
        world_info,
        fire_brigade_messages,
        channel_send_message_list,
        channel_size,
      )

    voice_message_low_list = []
    voice_message_normal_list = []
    voice_message_high_list = []

    for msg in voice_messages:
      if isinstance(msg, StandardMessage):
        if msg.get_priority() == StandardMessagePriority.LOW:
          voice_message_low_list.append(msg)
        elif msg.get_priority() == StandardMessagePriority.NORMAL:
          voice_message_normal_list.append(msg)
        elif msg.get_priority() == StandardMessagePriority.HIGH:
          voice_message_high_list.append(msg)

    channel_send_message_list[0].extend(voice_message_high_list)
    channel_send_message_list[0].extend(voice_message_normal_list)
    channel_send_message_list[0].extend(voice_message_low_list)

  def get_channels_by_agent_type(
    self,
    agent_type: EntityURN,
    agent_info: AgentInfo,
    world_info: WorldInfo,
    scenario_info: ScenarioInfo,
  ) -> list[int]:
    num_channels = (
      scenario_info.get_value(ScenarioInfoKeys.COMMUNICATION_CHANNELS_COUNT, 1) - 1
    )
    max_channel_count = int(
      # scenario_info.get_comms_channels_max_platoon()
      scenario_info.get_value(ScenarioInfoKeys.COMMUNICATION_CHANNELS_MAX_PLATOON, 1)
      if self.is_platoon_agent(agent_info, world_info)
      else scenario_info.get_value(
        ScenarioInfoKeys.COMMUNICATION_CHANNELS_MAX_OFFICE, 1
      )
    )
    channels = [
      DefaultChannelSubscriber.get_channel_number(agent_type, i, num_channels)
      for i in range(max_channel_count)
    ]
    return channels

  def is_platoon_agent(self, agent_info: AgentInfo, world_info: WorldInfo) -> bool:
    agent_type = self.get_agent_type(agent_info, world_info)
    return agent_type in [
      EntityURN.FIRE_BRIGADE,
      EntityURN.POLICE_FORCE,
      EntityURN.AMBULANCE_TEAM,
    ]

  def get_agent_type(
    self, agent_info: AgentInfo, world_info: WorldInfo
  ) -> Optional[EntityURN]:
    entity = world_info.get_entity(agent_info.get_entity_id())
    if entity is None:
      return None
    return entity.get_urn()

  def set_send_messages(
    self,
    scenario_info: ScenarioInfo,
    agent_type: EntityURN,
    agent_info: AgentInfo,
    world_info: WorldInfo,
    messages: list[StandardMessage],
    channel_send_message_list: list[list[CommunicationMessage]],
    channel_size: list[int],
  ) -> None:
    channels = self.get_channels_by_agent_type(
      agent_type, agent_info, world_info, scenario_info
    )
    channel_capacities = [
      scenario_info.get_value("comms.channels." + str(channel) + ".bandwidth", 0)
      for channel in range(
        scenario_info.get_value(ScenarioInfoKeys.COMMUNICATION_CHANNELS_COUNT, 1)
      )
    ]

    sorted_messages = sorted(
      messages, key=lambda x: x.get_priority().value, reverse=True
    )

    for message in sorted_messages:
      for channel in channels:
        if message not in channel_send_message_list[channel] and (
          (channel_size[channel] + message.get_bit_size())
          <= channel_capacities[channel]
        ):
          channel_size[channel] += message.get_bit_size()
          channel_send_message_list[channel].append(message)
          break
