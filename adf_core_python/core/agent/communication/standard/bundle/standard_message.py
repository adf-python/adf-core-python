from typing import Optional

from bitarray import bitarray
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
        priority: StandardMessagePriority,
        sender_id: int = -1,
        ttl: int = -1,
    ):
        super().__init__(is_wireless_message)
        self._priority = priority
        self._sender_id = sender_id
        self._ttl = ttl

    def get_sender_entity_id(self) -> EntityID:
        return EntityID(self._sender_id)

    def get_ttl(self) -> int:
        return self._ttl

    def get_priority(self) -> StandardMessagePriority:
        return self._priority

    @staticmethod
    def write_with_exist_flag(
        bit_array: bitarray, value: Optional[int], size: int
    ) -> None:
        if value is None:
            bit_array.extend([False])
        else:
            bit_array.extend([True])
            bit_array.frombytes(value.to_bytes(size, "big"))

    @staticmethod
    def read_with_exist_flag(bit_array: bitarray, size: int) -> Optional[int]:
        exist_flag = bit_array.pop(0)
        if exist_flag == 0:
            return None
        elif exist_flag == 1:
            value = int.from_bytes(bit_array.tobytes()[:size], "big")
            del bit_array[:size]
            return value
        else:
            raise ValueError("Invalid exist flag")
