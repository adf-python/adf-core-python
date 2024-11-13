from __future__ import annotations

from typing import Optional

from bitarray import bitarray
from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.communication.standard.bundle.standard_message_priority import (
    StandardMessagePriority,
)
from adf_core_python.core.agent.communication.standard.utility.bitarray_with_exits_flag import (
    read_with_exist_flag,
    write_with_exist_flag,
)
from adf_core_python.core.component.communication.communication_message import (
    CommunicationMessage,
)


class StandardMessage(CommunicationMessage):
    SIZE_TTL: int = 3

    def __init__(
        self,
        is_wireless_message: bool,
        priority: StandardMessagePriority,
        sender_entity_id: EntityID,
        ttl: Optional[int] = None,
    ):
        super().__init__(is_wireless_message)
        self._priority = priority
        self._sender_entity_id = sender_entity_id
        self._ttl = ttl

    def get_sender_entity_id(self) -> EntityID:
        return self._sender_entity_id

    def get_priority(self) -> StandardMessagePriority:
        return self._priority

    def get_ttl(self) -> Optional[int]:
        return self._ttl

    @classmethod
    def from_bits(
        cls,
        bit_array: bitarray,
        is_wireless_message: bool,
        sender_entity_id: EntityID,
    ) -> StandardMessage:
        ttl = read_with_exist_flag(bit_array, cls.SIZE_TTL)
        return StandardMessage(
            is_wireless_message,
            StandardMessagePriority.NORMAL,
            sender_entity_id,
            ttl,
        )

    def to_bits(self) -> bitarray:
        bit_array = bitarray()
        write_with_exist_flag(bit_array, self._ttl, self.SIZE_TTL)
        return bit_array

    def get_bit_size(self) -> int:
        raise NotImplementedError

    def __hash__(self) -> int:
        return hash((self._sender_entity_id, self._priority, self._ttl))

    def __str__(self) -> str:
        return f"StandardMessage(sender_entity_id={self._sender_entity_id}, priority={self._priority}, ttl={self._ttl})"
