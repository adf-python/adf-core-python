from typing import Optional

from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.communication.standard.bundle.standard_message_priority import (
    StandardMessagePriority,
)
from adf_core_python.core.component.communication.communication_message import (
    CommunicationMessage,
)


class StandardMessage(CommunicationMessage):
    def __init__(
        self,
        is_wireless_message: bool,
        sender_id: int,
        ttl: int,
        priority: StandardMessagePriority,
    ):
        super().__init__(is_wireless_message)
        self._sender_id = sender_id
        self._ttl = ttl
        self._priority = priority

    def get_sender_entity_id(self) -> EntityID:
        return EntityID(self._sender_id)

    def get_ttl(self) -> int:
        return self._ttl

    def get_priority(self) -> StandardMessagePriority:
        return self._priority

    def write_with_exist_flag(
        self, byte_array: bytearray, value: Optional[int], size: int
    ) -> None:
        if value is None:
            byte_array.extend(b"\b0")
        else:
            byte_array.extend(b"\b1")
            byte_array.extend(value.to_bytes(size, "big"))

    def read_with_exist_flag(self, byte_array: bytearray, size: int) -> Optional[int]:
        exist_flag = byte_array.pop(0)
        if exist_flag == 0:
            return None
        elif exist_flag == 1:
            value = int.from_bytes(byte_array[:size], "big")
            del byte_array[:size]
            return value
        else:
            raise ValueError("Invalid exist flag")
