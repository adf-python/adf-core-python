from __future__ import annotations

from bitarray import bitarray
from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.communication.standard.bundle.standard_message import (
    StandardMessage,
)
from adf_core_python.core.agent.communication.standard.bundle.standard_message_priority import (
    StandardMessagePriority,
)
from adf_core_python.core.agent.communication.standard.utility.bitarray_with_exits_flag import (
    read_with_exist_flag,
    write_with_exist_flag,
)


class CommandReport(StandardMessage):
    SIZE_DONE: int = 1
    SIZE_BLOADCAST: int = 1

    def __init__(
        self,
        is_wireless_message: bool,
        is_done: bool,
        is_bloadcast: bool,
        sender_entity_id: EntityID,
        priority: StandardMessagePriority,
    ):
        super().__init__(is_wireless_message, priority, sender_entity_id)
        self._is_done: bool = is_done
        self._is_bloadcast: bool = is_bloadcast

    def is_done(self) -> bool:
        return self._is_done

    def is_broadcast(self) -> bool:
        return self._is_bloadcast

    def get_bit_size(self) -> int:
        return self.to_bits().__len__()

    def to_bits(self) -> bitarray:
        bit_array = super().to_bits()
        write_with_exist_flag(
            bit_array,
            self._is_done,
            self.SIZE_DONE,
        )
        write_with_exist_flag(
            bit_array,
            self._is_bloadcast,
            self.SIZE_BLOADCAST,
        )
        return bit_array

    @classmethod
    def from_bits(
        cls,
        bit_array: bitarray,
        is_wireless_message: bool,
        sender_entity_id: EntityID,
    ) -> CommandReport:
        std_message = super().from_bits(
            bit_array, is_wireless_message, sender_entity_id
        )
        is_done = read_with_exist_flag(bit_array, cls.SIZE_DONE) == 1
        is_bloadcast = read_with_exist_flag(bit_array, cls.SIZE_BLOADCAST) == 1
        return cls(
            is_wireless_message,
            is_done,
            is_bloadcast,
            std_message.get_sender_entity_id(),
            std_message.get_priority(),
        )

    def __hash__(self):
        h = super().__hash__()
        return hash(
            (
                h,
                self._is_done,
                self._is_bloadcast,
            )
        )

    def __str__(self) -> str:
        return f"CommandReport(done={self._is_done}, broadcast={self._is_bloadcast})"
