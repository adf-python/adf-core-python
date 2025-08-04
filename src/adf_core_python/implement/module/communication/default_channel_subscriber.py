from __future__ import annotations

from typing import TYPE_CHECKING

from rcrscore.urn import EntityURN

from adf_core_python.core.agent.info.scenario_info import ScenarioInfoKeys
from adf_core_python.core.component.communication.channel_subscriber import (
    ChannelSubscriber,
)

if TYPE_CHECKING:
    from adf_core_python.core.agent.info.agent_info import AgentInfo
    from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
    from adf_core_python.core.agent.info.world_info import WorldInfo


class DefaultChannelSubscriber(ChannelSubscriber):
    def subscribe(
        self,
        agent_info: AgentInfo,
        world_info: WorldInfo,
        scenario_info: ScenarioInfo,
    ) -> list[int]:
        agent = world_info.get_entity(agent_info.get_entity_id())
        if agent is None:
            return []

        agent_type = agent.get_urn()

        number_of_channels: int = (
            scenario_info.get_value(ScenarioInfoKeys.COMMUNICATION_CHANNELS_COUNT, 1)
            - 1
        )

        is_platoon: bool = (
            agent_type == EntityURN.FIRE_BRIGADE
            or agent_type == EntityURN.POLICE_FORCE
            or agent_type == EntityURN.AMBULANCE_TEAM
        )

        max_channel_count: int = (
            scenario_info.get_value(
                ScenarioInfoKeys.COMMUNICATION_CHANNELS_MAX_PLATOON, 1
            )
            if is_platoon
            else scenario_info.get_value(
                ScenarioInfoKeys.COMMUNICATION_CHANNELS_MAX_OFFICE, 1
            )
        )

        channels = [
            self.get_channel_number(agent_type, i, number_of_channels)
            for i in range(max_channel_count)
        ]
        return channels

    @staticmethod
    def get_channel_number(
        agent_type: EntityURN, channel_index: int, number_of_channels: int
    ) -> int:
        agent_index = 0
        if agent_type == EntityURN.FIRE_BRIGADE or agent_type == EntityURN.FIRE_STATION:
            agent_index = 1
        elif (
            agent_type == EntityURN.POLICE_FORCE
            or agent_type == EntityURN.POLICE_OFFICE
        ):
            agent_index = 2
        elif (
            agent_type == EntityURN.AMBULANCE_TEAM
            or agent_type == EntityURN.AMBULANCE_CENTER
        ):
            agent_index = 3

        index = (3 * channel_index) + agent_index
        if (index % number_of_channels) == 0:
            index = number_of_channels
        else:
            index = index % number_of_channels
        return index


if __name__ == "__main__":
    num_channels = 1
    max_channels = 2

    for i in range(max_channels):
        print(
            f"FIREBRIGADE-{i}: {DefaultChannelSubscriber.get_channel_number(EntityURN.FIRE_BRIGADE, i, num_channels)}"
        )

    for i in range(max_channels):
        print(
            f"POLICE-{i}: {DefaultChannelSubscriber.get_channel_number(EntityURN.POLICE_OFFICE, i, num_channels)}"
        )

    for i in range(max_channels):
        print(
            f"AMB-{i}: {DefaultChannelSubscriber.get_channel_number(EntityURN.AMBULANCE_CENTER, i, num_channels)}"
        )
