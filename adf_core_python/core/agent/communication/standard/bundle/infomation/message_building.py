from __future__ import annotations

from typing import Optional

from bitarray import bitarray
from rcrs_core.entities.building import Building
from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.communication.standard.bundle.standard_message import (
    StandardMessage,
)
from adf_core_python.core.agent.communication.standard.bundle.standard_message_priority import (
    StandardMessagePriority,
)


class MessageBuilding(StandardMessage):
    SIZE_BUILDING_ENTITY_ID: int = 32
    SIZE_BUILDING_BROKENNESS: int = 32
    SIZE_BUILDING_FIREYNESS: int = 32
    SIZE_BUILDING_TEMPERATURE: int = 32

    def __init__(
        self,
        is_wireless_message: bool,
        building: Building,
        priority: StandardMessagePriority = StandardMessagePriority.NORMAL,
        sender_id: int = -1,
        ttl: int = -1,
    ):
        super().__init__(is_wireless_message, priority, sender_id, ttl)
        self._building_entity_id: Optional[EntityID] = building.get_id()
        self._building_brokenness: Optional[int] = building.get_brokenness() or None
        self._building_fireyness: Optional[int] = building.get_fieryness() or None
        self._building_temperature: Optional[int] = building.get_temperature() or None

    def get_byte_size(self) -> int:
        return self.to_bytes().__len__()

    def to_bytes(self) -> bytes:
        bit_array = bitarray()
        self.write_with_exist_flag(
            bit_array,
            self._building_entity_id.get_value() if self._building_entity_id else None,
            self.SIZE_BUILDING_ENTITY_ID,
        )
        self.write_with_exist_flag(
            bit_array,
            self._building_brokenness,
            self.SIZE_BUILDING_BROKENNESS,
        )
        self.write_with_exist_flag(
            bit_array,
            self._building_fireyness,
            self.SIZE_BUILDING_FIREYNESS,
        )
        self.write_with_exist_flag(
            bit_array,
            self._building_temperature,
            self.SIZE_BUILDING_TEMPERATURE,
        )
        return bit_array.tobytes()

    @classmethod
    def from_bytes(cls, bytes: bytes) -> MessageBuilding:
        bit_array = bitarray()
        bit_array.frombytes(bytes)
        raw_building_entity_id = cls.read_with_exist_flag(
            bit_array, cls.SIZE_BUILDING_ENTITY_ID
        )
        building_entity_id = (
            EntityID(raw_building_entity_id) if raw_building_entity_id else None
        )
        building_brokenness = cls.read_with_exist_flag(
            bit_array, cls.SIZE_BUILDING_BROKENNESS
        )
        building_fireyness = cls.read_with_exist_flag(
            bit_array, cls.SIZE_BUILDING_FIREYNESS
        )
        building_temperature = cls.read_with_exist_flag(
            bit_array, cls.SIZE_BUILDING_TEMPERATURE
        )
        building = Building(
            building_entity_id.get_value() if building_entity_id else None
        )
        building.set_brokenness(building_brokenness)
        building.set_fieryness(building_fireyness)
        building.set_temperature(building_temperature)
        return MessageBuilding(
            False,
            building,
        )

    def get_check_key(self) -> str:
        building_entity_id_value = (
            self._building_entity_id.get_value() if self._building_entity_id else None
        )
        return f"{self.__class__.__name__} > building: {building_entity_id_value}"

    def get_building_entity_id(self) -> Optional[EntityID]:
        return self._building_entity_id

    def get_building_brokenness(self) -> Optional[int]:
        return self._building_brokenness

    def get_building_fireyness(self) -> Optional[int]:
        return self._building_fireyness

    def get_building_temperature(self) -> Optional[int]:
        return self._building_temperature
