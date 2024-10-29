from __future__ import annotations

from typing import TYPE_CHECKING

from bitarray import bitarray
from rcrs_core.commands.AKSpeak import AKSpeak
from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.communication.message_manager import MessageManager
from adf_core_python.core.agent.communication.standard.bundle.standard_message import (
    StandardMessage,
)
from adf_core_python.core.agent.communication.standard.utility.bitarray_with_exits_flag import (
    read_with_exist_flag,
    write_with_exist_flag,
)
from adf_core_python.core.component.communication.communication_module import (
    CommunicationModule,
)
from adf_core_python.core.logger.logger import get_logger

if TYPE_CHECKING:
    from adf_core_python.core.agent.agent import Agent


class StandardCommunicationModule(CommunicationModule):
    ESCAPE_CHAR = bitarray("11111111")
    SIZE_ID: int = 5
    SIZE_TTL: int = 3

    def receive(self, agent: Agent, message_manager: MessageManager) -> None:
        heard_commands = agent._agent_info.get_heard_commands()
        for command in heard_commands:
            if isinstance(command, AKSpeak):
                sender_entity_id = command.agent_id
                if sender_entity_id == agent.get_entity_id():
                    continue
                data = command.message
                is_wireless_message = command.channel != 0

                if len(data) == 0:
                    continue

                if is_wireless_message:
                    bit_array = bitarray()
                    bit_array.frombytes(data)
                    self.add_received_message(
                        message_manager,
                        is_wireless_message,
                        sender_entity_id,
                        bit_array,
                    )
                else:
                    try:
                        voice_message = data.decode("utf-8")
                        if voice_message.startswith("Help") or voice_message.startswith(
                            "Ouch"
                        ):
                            message_manager.add_heard_agent_help_message_count()
                            continue
                    except UnicodeDecodeError:
                        pass

                    escape_char = self.ESCAPE_CHAR.tobytes()[0]
                    i = 0
                    bit_array = bitarray()
                    a = bitarray()
                    a.frombytes(data)
                    while i < len(data):
                        if data[i] == escape_char:
                            if (i + 1) >= len(data):
                                self.add_received_message(
                                    message_manager,
                                    False,
                                    sender_entity_id,
                                    bit_array,
                                )
                                break
                            elif data[i + 1] != escape_char:
                                self.add_received_message(
                                    message_manager,
                                    False,
                                    sender_entity_id,
                                    bit_array,
                                )
                                bit_array.clear()
                                i += 1  # Skip the next character
                                continue
                            i += 1  # Skip the escaped character
                        bits = bitarray()
                        bits.frombytes(data[i].to_bytes(1, "big"))
                        bit_array.extend(bits)
                        i += 1

    def send(self, agent: Agent, message_manager: MessageManager) -> None:
        voice_message_limit_bytes = agent._scenario_info.get_value(
            "comms.channels.0.messages.size", 256
        )
        left_voice_message_limit_bits = voice_message_limit_bytes * 8
        voice_message_bit_array = bitarray()

        send_messages = message_manager.get_channel_send_message_list()

        for channel in range(len(send_messages)):
            for message in send_messages[channel]:
                message_class_index = message_manager.get_message_class_index(
                    type(message)
                )
                bit_array = bitarray()

                write_with_exist_flag(bit_array, message_class_index, self.SIZE_ID)

                bit_array.extend(message.to_bits())

                if channel > 0:
                    agent.send_speak(
                        agent._agent_info.get_time(),
                        bit_array,
                        channel,
                    )
                else:
                    # bit_arrayを8bitごとに区切れるようにして、エスケープ処理を行う
                    if len(bit_array) % 8 != 0:
                        bit_array.extend([False] * (8 - len(bit_array) % 8))
                    message_bit_size = len(bit_array)
                    if message_bit_size <= left_voice_message_limit_bits:
                        esceped_message_data = bitarray()
                        for i in range(len(bit_array) // 8):
                            if bit_array[(i * 8) : ((i + 1) * 8)] == self.ESCAPE_CHAR:
                                esceped_message_data.extend(self.ESCAPE_CHAR)
                            esceped_message_data.extend(
                                bit_array[(i * 8) : ((i + 1) * 8)]
                            )
                        esceped_message_data.extend(self.ESCAPE_CHAR)
                        if len(esceped_message_data) <= voice_message_limit_bytes:
                            left_voice_message_limit_bits -= len(esceped_message_data)
                            voice_message_bit_array.extend(esceped_message_data)

        if len(voice_message_bit_array) > 0:
            agent.send_speak(
                agent._agent_info.get_time(),
                voice_message_bit_array,
                0,
            )

    def add_received_message(
        self,
        message_manager: MessageManager,
        is_wireless_message: bool,
        sender_entity_id: EntityID,
        data: bitarray,
    ) -> None:
        message_class_index = read_with_exist_flag(data, self.SIZE_ID)
        if message_class_index is None or message_class_index < 0:
            get_logger(
                f"{self.__class__.__module__}.{self.__class__.__qualname__}"
            ).warning(f"Invalid message class index: {message_class_index}")
            return

        message = message_manager.get_message_class(message_class_index)
        if message is None:
            get_logger(
                f"{self.__class__.__module__}.{self.__class__.__qualname__}"
            ).warning(f"Invalid message class index: {message_class_index}")
            return

        if issubclass(message, StandardMessage):
            message_instance = message.from_bits(
                data, is_wireless_message, sender_entity_id
            )
            message_manager.add_received_message(message_instance)
        else:
            get_logger(
                f"{self.__class__.__module__}.{self.__class__.__qualname__}"
            ).warning(f"Invalid message class: {message}")
            return
