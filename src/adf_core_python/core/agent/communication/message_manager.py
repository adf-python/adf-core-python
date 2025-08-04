from __future__ import annotations

from typing import TYPE_CHECKING

from adf_core_python.core.agent.info.scenario_info import ScenarioInfo, ScenarioInfoKeys
from adf_core_python.core.agent.info.world_info import WorldInfo

if TYPE_CHECKING:
    from adf_core_python.core.agent.info.agent_info import AgentInfo
    from adf_core_python.core.component.communication.channel_subscriber import (
        ChannelSubscriber,
    )
    from adf_core_python.core.component.communication.communication_message import (
        CommunicationMessage,
    )
    from adf_core_python.core.component.communication.message_coordinator import (
        MessageCoordinator,
    )


class MessageManager:
    MAX_MESSAGE_CLASS_COUNT = 32

    def __init__(self) -> None:
        """
        Initialize the MessageManager.

        Parameters
        ----------
        __standard_message_class_count : int
            The count of standard message classes.
        __custom_message_class_count : int
            The count of custom message classes.
        __message_classes : dict[int, CommunicationMessage]
            The message classes.
        __subscribed_channels : list[int]
            The subscribed channels. Default is [1].
        __is_subscribed : bool
            The flag to indicate if the agent is subscribed to the channel.
        """
        self.__standard_message_class_count = 0b0000_0001
        self.__custom_message_class_count = 0b0001_0000
        self.__message_classes: dict[int, type[CommunicationMessage]] = {}
        self.__send_message_list: list[CommunicationMessage] = []
        self.__received_message_list: list[CommunicationMessage] = []
        self.__channel_send_message_list: list[list[CommunicationMessage]] = []
        self.__check_duplicate_cache: set[int] = set()
        self.__message_coordinator: MessageCoordinator
        self.__channel_subscriber: ChannelSubscriber
        self.__heard_agent_help_message_count: int = 0
        self.__subscribed_channels: list[int] = [1]
        self.__is_subscribed = False

    def set_subscribed_channels(self, subscribed_channels: list[int]) -> None:
        """
        Set the subscribed channels.

        Parameters
        ----------
        subscribed_channels : list[int]
            The subscribed channels.

        """
        self.__subscribed_channels = subscribed_channels
        self.__is_subscribed = False

    def get_subscribed_channels(self) -> list[int]:
        """
        Get the subscribed channels.

        Returns
        -------
        list[int]
            The subscribed channels.

        """
        return self.__subscribed_channels

    def set_is_subscribed(self, is_subscribed: bool) -> None:
        """
        Set the flag to indicate if the agent is subscribed to the channel.

        Parameters
        ----------
        is_subscribed : bool
            The flag to indicate if the agent is subscribed to the channel.

        """
        self.__is_subscribed = is_subscribed

    def get_is_subscribed(self) -> bool:
        """
        Get the flag to indicate if the agent is subscribed to the channel.

        Returns
        -------
        bool
            The flag to indicate if the agent is subscribed to the channel.

        """
        return self.__is_subscribed

    def set_channel_subscriber(self, channel_subscriber: ChannelSubscriber) -> None:
        """
        Set the channel subscriber.

        Parameters
        ----------
        channel_subscriber : ChannelSubscriber
            The channel subscriber.

        """
        self.__channel_subscriber = channel_subscriber

    def set_message_coordinator(self, message_coordinator: MessageCoordinator) -> None:
        """
        Set the message coordinator.

        Parameters
        ----------
        message_coordinator : MessageCoordinator
            The message coordinator.

        """
        self.__message_coordinator = message_coordinator

    def get_channel_subscriber(self) -> ChannelSubscriber:
        """
        Get the channel subscriber.

        Returns
        -------
        ChannelSubscriber
            The channel subscriber.

        """
        return self.__channel_subscriber

    def add_heard_agent_help_message_count(self) -> None:
        """
        Add the heard agent help message count.

        """
        self.__heard_agent_help_message_count += 1

    def get_heard_agent_help_message_count(self) -> int:
        """
        Get the heard agent help message count.

        Returns
        -------
        int
            The heard agent help message count.

        """
        return self.__heard_agent_help_message_count

    def add_received_message(self, message: CommunicationMessage) -> None:
        """
        Add the received message.

        Parameters
        ----------
        message : CommunicationMessage
            The received message.

        """
        self.__received_message_list.append(message)

    def get_received_message_list(self) -> list[CommunicationMessage]:
        """
        Get the received message list.

        Returns
        -------
        list[CommunicationMessage]
            The received message list.

        """
        return self.__received_message_list

    def get_channel_send_message_list(self) -> list[list[CommunicationMessage]]:
        """
        Get the channel send message list.

        Returns
        -------
        list[list[CommunicationMessage]]
            The channel send message list.

        """
        return self.__channel_send_message_list

    def subscribe(
        self, agent_info: AgentInfo, world_info: WorldInfo, scenario_info: ScenarioInfo
    ) -> None:
        """
        Subscribe to the channel.

        Parameters
        ----------
        agent_info : AgentInfo
            The agent info.
        world_info : WorldInfo
            The world info.
        scenario_info : ScenarioInfo
            The scenario info.

        Throws
        ------
        ValueError
            If the ChannelSubscriber is not set.

        """
        if self.__channel_subscriber is None:
            raise ValueError("ChannelSubscriber is not set.")

        if agent_info.get_time() == 1:
            self.__subscribed_channels = self.__channel_subscriber.subscribe(
                agent_info, world_info, scenario_info
            )

    def register_message_class(
        self, index: int, message_class: type[CommunicationMessage]
    ) -> None:
        """
        Register the message class.

        Parameters
        ----------
        message_class : type[CommunicationMessage]
            The message class.

        """
        if index >= self.MAX_MESSAGE_CLASS_COUNT:
            raise ValueError(
                f"Possible index values are 0 to {self.MAX_MESSAGE_CLASS_COUNT - 1}"
            )
        self.__message_classes[index] = message_class

    def get_message_class(self, index: int) -> type[CommunicationMessage]:
        """
        Get the message class.

        Parameters
        ----------
        index : int
            The index.

        Returns
        -------
        type[CommunicationMessage]
            The message class.

        """
        return self.__message_classes[index]

    def get_message_class_index(self, message_class: type[CommunicationMessage]) -> int:
        """
        Get the message class index.

        Parameters
        ----------
        message_class : type[CommunicationMessage]
            The message class.

        Returns
        -------
        int
            The message class index.

        """
        for index, cls in self.__message_classes.items():
            if cls == message_class:
                return index
        return -1

    def add_message(
        self, message: CommunicationMessage, check_duplicate: bool = True
    ) -> None:
        """
        Add the message.

        Parameters
        ----------
        message : CommunicationMessage
            The message.

        """
        check_key = message.__hash__()
        # TODO:両方同じコードになっているが、なぜなのか調査する
        if check_duplicate and check_key not in self.__check_duplicate_cache:
            self.__send_message_list.append(message)
            self.__check_duplicate_cache.add(check_key)
        else:
            self.__send_message_list.append(message)
            self.__check_duplicate_cache.add(check_key)

    def get_send_message_list(self) -> list[CommunicationMessage]:
        """
        Get the send message list.

        Returns
        -------
        list[CommunicationMessage]
            The send message list.

        """
        return self.__send_message_list

    def coordinate_message(
        self, agent_info: AgentInfo, world_info: WorldInfo, scenario_info: ScenarioInfo
    ) -> None:
        """
        Coordinate the message.

        Parameters
        ----------
        agent_info : AgentInfo
            The agent info.
        world_info : WorldInfo
            The world info.
        scenario_info : ScenarioInfo
            The scenario info.

        """
        if self.__message_coordinator is None:
            raise ValueError("MessageCoordinator is not set.")

        self.__channel_send_message_list = [
            []
            for _ in range(
                int(
                    scenario_info.get_value(
                        ScenarioInfoKeys.COMMUNICATION_CHANNELS_COUNT, 1
                    )
                )
            )
        ]

        self.__message_coordinator.coordinate(
            agent_info,
            world_info,
            scenario_info,
            self,
            self.__send_message_list,
            self.__channel_send_message_list,
        )

    def refresh(self) -> None:
        """
        Refresh the message manager.

        """
        self.__send_message_list = []
        self.__received_message_list = []
        self.__check_duplicate_cache = set()
        self.__heard_agent_help_message_count = 0

    def __str__(self) -> str:
        return (
            f"MessageManager("
            f"standard_message_class_count={self.__standard_message_class_count}, "
            f"custom_message_class_count={self.__custom_message_class_count}, "
            f"message_classes={self.__message_classes}, "
            f"send_message_list={self.__send_message_list}, "
            f"received_message_list={self.__received_message_list}, "
            f"channel_send_message_list={self.__channel_send_message_list}, "
            f"check_duplicate_cache={self.__check_duplicate_cache}, "
            f"message_coordinator={self.__message_coordinator}, "
            f"channel_subscriber={self.__channel_subscriber}, "
            f"heard_agent_help_message_count={self.__heard_agent_help_message_count}, "
            f"subscribed_channels={self.__subscribed_channels}, "
            f"is_subscribed={self.__is_subscribed})"
        )
