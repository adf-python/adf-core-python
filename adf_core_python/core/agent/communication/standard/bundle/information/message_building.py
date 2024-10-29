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
from adf_core_python.core.agent.communication.standard.utility.bitarray_with_exits_flag import (
    read_with_exist_flag,
    write_with_exist_flag,
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
        priority: StandardMessagePriority,
        sender_entity_id: EntityID,
        ttl: Optional[int] = None,
    ):
        super().__init__(is_wireless_message, priority, sender_entity_id, ttl)
        self._building_entity_id: Optional[EntityID] = building.get_id()
        self._building_brokenness: Optional[int] = building.get_brokenness() or None
        self._building_fireyness: Optional[int] = building.get_fieryness() or None
        self._building_temperature: Optional[int] = building.get_temperature() or None

    def get_building_entity_id(self) -> Optional[EntityID]:
        return self._building_entity_id

    def get_building_brokenness(self) -> Optional[int]:
        return self._building_brokenness

    def get_building_fireyness(self) -> Optional[int]:
        return self._building_fireyness

    def get_building_temperature(self) -> Optional[int]:
        return self._building_temperature

    def get_bit_size(self) -> int:
        return self.to_bits().__len__()

    def to_bits(self) -> bitarray:
        bit_array = super().to_bits()
        write_with_exist_flag(
            bit_array,
            self._building_entity_id.get_value() if self._building_entity_id else None,
            self.SIZE_BUILDING_ENTITY_ID,
        )
        write_with_exist_flag(
            bit_array,
            self._building_brokenness,
            self.SIZE_BUILDING_BROKENNESS,
        )
        write_with_exist_flag(
            bit_array,
            self._building_fireyness,
            self.SIZE_BUILDING_FIREYNESS,
        )
        write_with_exist_flag(
            bit_array,
            self._building_temperature,
            self.SIZE_BUILDING_TEMPERATURE,
        )
        return bit_array

    @classmethod
    def from_bits(
        cls, bit_array: bitarray, is_wireless_message: bool, sender_entity_id: EntityID
    ) -> MessageBuilding:
        std_message = super().from_bits(
            bit_array, is_wireless_message, sender_entity_id
        )
        building_id = read_with_exist_flag(bit_array, cls.SIZE_BUILDING_ENTITY_ID)
        building_brokenness = read_with_exist_flag(
            bit_array, cls.SIZE_BUILDING_BROKENNESS
        )
        building_fireyness = read_with_exist_flag(
            bit_array, cls.SIZE_BUILDING_FIREYNESS
        )
        building_temperature = read_with_exist_flag(
            bit_array, cls.SIZE_BUILDING_TEMPERATURE
        )
        building = Building(building_id or -1)
        building.set_brokenness(building_brokenness)
        building.set_fieryness(building_fireyness)
        building.set_temperature(building_temperature)
        return MessageBuilding(
            False,
            building,
            StandardMessagePriority.NORMAL,
            sender_entity_id,
            std_message.get_ttl(),
        )

    def __hash__(self):
        h = super().__hash__()
        return hash(
            (
                h,
                self._building_entity_id,
                self._building_brokenness,
                self._building_fireyness,
                self._building_temperature,
            )
        )

    def __str__(self):
        return f"MessageBuilding(building_entity_id={self._building_entity_id}, building_brokenness={self._building_brokenness}, building_fireyness={self._building_fireyness}, building_temperature={self._building_temperature})"
