from __future__ import annotations

from typing import Optional

from bitarray import bitarray
from rcrs_core.entities.blockade import Blockade
from rcrs_core.entities.road import Road
from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.communication.standard.bundle.standard_message import (
    StandardMessage,
)
from adf_core_python.core.agent.communication.standard.bundle.standard_message_priority import (
    StandardMessagePriority,
)


class MessageRoad(StandardMessage):
    CTION_REST: int = 0
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
        priority: StandardMessagePriority = StandardMessagePriority.NORMAL,
        sender_id: int = -1,
        ttl: int = -1,
    ):
        super().__init__(is_wireless_message, priority, sender_id, ttl)
        self._road_entity_id: Optional[EntityID] = road.get_id()
        self._road_blockade_entity_id: Optional[EntityID] = None
        self._road_blockade_repair_cost: Optional[int] = None
        self._road_blockade_x: Optional[int] = None
        self._road_blockade_y: Optional[int] = None

        if blockade:
            self._road_blockade_entity_id = blockade.get_id()
            self._road_blockade_repair_cost = blockade.get_repaire_cost()
            if is_send_blockade_location:
                self._road_blockade_x = blockade.get_x() or None
                self._road_blockade_y = blockade.get_y() or None

        self._is_passable: Optional[bool] = is_passable
        self._is_send_blockade_location: bool = is_send_blockade_location

    def get_byte_size(self) -> int:
        return self.to_bytes().__len__()

    def to_bytes(self) -> bytes:
        bit_array = bitarray()
        self.write_with_exist_flag(
            bit_array,
            self._road_entity_id.get_value() if self._road_entity_id else None,
            self.SIZE_ROAD_ENTITY_ID,
        )
        self.write_with_exist_flag(
            bit_array,
            self._road_blockade_entity_id.get_value()
            if self._road_blockade_entity_id
            else None,
            self.SIZE_ROAD_BLOCKADE_ENTITY_ID,
        )
        self.write_with_exist_flag(
            bit_array,
            self._road_blockade_repair_cost
            if self._road_blockade_repair_cost
            else None,
            self.SIZE_ROAD_BLOCKADE_REPAIR_COST,
        )
        if self._is_send_blockade_location:
            self.write_with_exist_flag(
                bit_array,
                self._road_blockade_x if self._road_blockade_x else None,
                self.SIZE_ROAD_BLOCKADE_X,
            )
            self.write_with_exist_flag(
                bit_array,
                self._road_blockade_y if self._road_blockade_y else None,
                self.SIZE_ROAD_BLOCKADE_Y,
            )
        else:
            self.write_with_exist_flag(bit_array, None, self.SIZE_ROAD_BLOCKADE_X)
            self.write_with_exist_flag(bit_array, None, self.SIZE_ROAD_BLOCKADE_Y)
        self.write_with_exist_flag(
            bit_array,
            self._is_passable if self._is_passable else None,
            self.SIZE_PASSABLE,
        )
        return bit_array.tobytes()

    @classmethod
    def from_bytes(cls, bytes: bytes) -> MessageRoad:
        bit_array = bitarray()
        bit_array.frombytes(bytes)
        raw_road_entity_id = cls.read_with_exist_flag(
            bit_array, cls.SIZE_ROAD_ENTITY_ID
        )
        road_entity_id = EntityID(raw_road_entity_id) if raw_road_entity_id else None
        raw_road_blockade_entity_id = cls.read_with_exist_flag(
            bit_array, cls.SIZE_ROAD_BLOCKADE_ENTITY_ID
        )
        road_blockade_entity_id = (
            EntityID(raw_road_blockade_entity_id)
            if raw_road_blockade_entity_id
            else None
        )
        road_blockade_repair_cost = cls.read_with_exist_flag(
            bit_array, cls.SIZE_ROAD_BLOCKADE_REPAIR_COST
        )
        road_blockade_x = cls.read_with_exist_flag(bit_array, cls.SIZE_ROAD_BLOCKADE_X)
        road_blockade_y = cls.read_with_exist_flag(bit_array, cls.SIZE_ROAD_BLOCKADE_Y)
        is_passable = (
            True if cls.read_with_exist_flag(bit_array, cls.SIZE_PASSABLE) else False
        )
        road = Road(road_entity_id.get_value() if road_entity_id else None)
        blockade = Blockade(
            road_blockade_entity_id.get_value() if road_blockade_entity_id else None
        )
        blockade.set_repaire_cost(road_blockade_repair_cost)
        blockade.set_x(road_blockade_x)
        blockade.set_y(road_blockade_y)
        return MessageRoad(
            False,
            road,
            False,
            is_passable,
            blockade,
        )

    def get_check_key(self) -> str:
        road_entity_id_value = (
            self._road_entity_id.get_value() if self._road_entity_id else None
        )
        return f"{self.__class__.__name__} > road: {road_entity_id_value}"

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
