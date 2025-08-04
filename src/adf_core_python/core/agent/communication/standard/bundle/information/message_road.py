from __future__ import annotations

from typing import Optional

from bitarray import bitarray
from rcrscore.entities import Blockade, EntityID, Road

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


class MessageRoad(StandardMessage):
    ACTION_REST: int = 0
    ACTION_MOVE: int = 1
    ACTION_CLEAR: int = 2

    SIZE_ROAD_ENTITY_ID: int = 32
    SIZE_ROAD_BLOCKADE_ENTITY_ID: int = 32
    SIZE_ROAD_BLOCKADE_REPAIR_COST: int = 32
    SIZE_ROAD_BLOCKADE_X: int = 32
    SIZE_ROAD_BLOCKADE_Y: int = 32
    SIZE_PASSABLE: int = 1

    def __init__(
        self,
        is_wireless_message: bool,
        road: Road,
        is_send_blockade_location: bool,
        is_passable: Optional[bool],
        blockade: Optional[Blockade],
        priority: StandardMessagePriority,
        sender_entity_id: EntityID,
        ttl: Optional[int] = None,
    ):
        super().__init__(is_wireless_message, priority, sender_entity_id, ttl)
        self._road_entity_id: Optional[EntityID] = road.get_entity_id()
        self._road_blockade_entity_id: Optional[EntityID] = None
        self._road_blockade_repair_cost: Optional[int] = None
        self._road_blockade_x: Optional[int] = None
        self._road_blockade_y: Optional[int] = None

        if blockade:
            self._road_blockade_entity_id = blockade.get_entity_id()
            self._road_blockade_repair_cost = blockade.get_repair_cost()
            if is_send_blockade_location:
                self._road_blockade_x = blockade.get_x() or None
                self._road_blockade_y = blockade.get_y() or None

        self._is_passable: Optional[bool] = is_passable
        self._is_send_blockade_location: bool = is_send_blockade_location

    def get_road_entity_id(self) -> Optional[EntityID]:
        return self._road_entity_id

    def get_road_blockade_entity_id(self) -> Optional[EntityID]:
        return self._road_blockade_entity_id

    def get_road_blockade_repair_cost(self) -> Optional[int]:
        return self._road_blockade_repair_cost

    def get_road_blockade_x(self) -> Optional[int]:
        return self._road_blockade_x

    def get_road_blockade_y(self) -> Optional[int]:
        return self._road_blockade_y

    def get_is_passable(self) -> Optional[bool]:
        return self._is_passable

    def get_is_send_blockade_location(self) -> bool:
        return self._is_send_blockade_location

    def get_bit_size(self) -> int:
        return self.to_bits().__len__()

    def to_bits(self) -> bitarray:
        bit_array = super().to_bits()
        write_with_exist_flag(
            bit_array,
            self._road_entity_id.get_value() if self._road_entity_id else None,
            self.SIZE_ROAD_ENTITY_ID,
        )
        write_with_exist_flag(
            bit_array,
            self._road_blockade_entity_id.get_value()
            if self._road_blockade_entity_id
            else None,
            self.SIZE_ROAD_BLOCKADE_ENTITY_ID,
        )
        write_with_exist_flag(
            bit_array,
            self._road_blockade_repair_cost
            if self._road_blockade_repair_cost
            else None,
            self.SIZE_ROAD_BLOCKADE_REPAIR_COST,
        )
        if self._is_send_blockade_location:
            write_with_exist_flag(
                bit_array,
                self._road_blockade_x if self._road_blockade_x else None,
                self.SIZE_ROAD_BLOCKADE_X,
            )
            write_with_exist_flag(
                bit_array,
                self._road_blockade_y if self._road_blockade_y else None,
                self.SIZE_ROAD_BLOCKADE_Y,
            )
        else:
            write_with_exist_flag(bit_array, None, self.SIZE_ROAD_BLOCKADE_X)
            write_with_exist_flag(bit_array, None, self.SIZE_ROAD_BLOCKADE_Y)
        write_with_exist_flag(
            bit_array,
            self._is_passable if self._is_passable else None,
            self.SIZE_PASSABLE,
        )
        return bit_array

    @classmethod
    def from_bits(
        cls, bit_array: bitarray, is_wireless_message: bool, sender_entity_id: EntityID
    ) -> MessageRoad:
        std_message = super().from_bits(
            bit_array, is_wireless_message, sender_entity_id
        )
        road_id = read_with_exist_flag(bit_array, cls.SIZE_ROAD_ENTITY_ID)
        road_blockade_id = read_with_exist_flag(
            bit_array, cls.SIZE_ROAD_BLOCKADE_ENTITY_ID
        )
        road_blockade_repair_cost = read_with_exist_flag(
            bit_array, cls.SIZE_ROAD_BLOCKADE_REPAIR_COST
        )
        road_blockade_x = read_with_exist_flag(bit_array, cls.SIZE_ROAD_BLOCKADE_X)
        road_blockade_y = read_with_exist_flag(bit_array, cls.SIZE_ROAD_BLOCKADE_Y)
        is_passable = (
            True if read_with_exist_flag(bit_array, cls.SIZE_PASSABLE) else False
        )
        road = Road(road_id or -1)
        blockade = Blockade(road_blockade_id or -1)
        blockade.set_repair_cost(road_blockade_repair_cost)
        blockade.set_x(road_blockade_x)
        blockade.set_y(road_blockade_y)
        return MessageRoad(
            is_wireless_message,
            road,
            False,
            is_passable,
            blockade,
            StandardMessagePriority.NORMAL,
            sender_entity_id,
            std_message.get_ttl(),
        )

    def __hash__(self) -> int:
        h = super().__hash__()
        return hash(
            (
                h,
                self._road_entity_id,
                self._road_blockade_entity_id,
                self._road_blockade_repair_cost,
                self._road_blockade_x,
                self._road_blockade_y,
                self._is_passable,
                self._is_send_blockade_location,
            )
        )

    def __str__(self) -> str:
        return f"MessageRoad(road_entity_id={self._road_entity_id}, road_blockade_entity_id={self._road_blockade_entity_id}, road_blockade_repair_cost={self._road_blockade_repair_cost}, road_blockade_x={self._road_blockade_x}, road_blockade_y={self._road_blockade_y}, is_passable={self._is_passable}, is_send_blockade_location={self._is_send_blockade_location})"
