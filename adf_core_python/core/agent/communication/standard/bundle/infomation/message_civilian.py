from __future__ import annotations

from typing import Optional

from bitarray import bitarray
from rcrs_core.entities.civilian import Civilian
from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.communication.standard.bundle.standard_message import (
    StandardMessage,
)
from adf_core_python.core.agent.communication.standard.bundle.standard_message_priority import (
    StandardMessagePriority,
)


class MessageCivilian(StandardMessage):
    SIZE_CIVILIAN_ENTITY_ID: int = 32
    SIZE_CIVILIAN_HP: int = 14
    SIZE_CIVILIAN_BURIEDNESS: int = 13
    SIZE_CIVILIAN_DAMAGE: int = 14
    SIZE_CIVILIAN_POSITION: int = 32

    def __init__(
        self,
        is_wireless_message: bool,
        civilian: Civilian,
        priority: StandardMessagePriority = StandardMessagePriority.NORMAL,
        sender_id: int = -1,
        ttl: int = -1,
    ):
        super().__init__(is_wireless_message, priority, sender_id, ttl)
        self._civilian_entity_id: Optional[EntityID] = civilian.get_id()
        self._civilian_hp: Optional[int] = civilian.get_hp() or None
        self._civilian_buriedness: Optional[int] = civilian.get_buriedness() or None
        self._civilian_damage: Optional[int] = civilian.get_damage() or None
        self._civilian_position: Optional[EntityID] = civilian.get_position() or None

    def get_byte_size(self) -> int:
        return self.to_bytes().__len__()

    def to_bytes(self) -> bytes:
        bit_array = bitarray()
        self.write_with_exist_flag(
            bit_array,
            self._civilian_entity_id.get_value() if self._civilian_entity_id else None,
            self.SIZE_CIVILIAN_ENTITY_ID,
        )
        self.write_with_exist_flag(
            bit_array,
            self._civilian_hp,
            self.SIZE_CIVILIAN_HP,
        )
        self.write_with_exist_flag(
            bit_array,
            self._civilian_buriedness,
            self.SIZE_CIVILIAN_BURIEDNESS,
        )
        self.write_with_exist_flag(
            bit_array,
            self._civilian_damage,
            self.SIZE_CIVILIAN_DAMAGE,
        )
        self.write_with_exist_flag(
            bit_array,
            self._civilian_position.get_value() if self._civilian_position else None,
            self.SIZE_CIVILIAN_POSITION,
        )
        return bit_array.tobytes()

    @classmethod
    def from_bytes(cls, bytes: bytes) -> MessageCivilian:
        bit_array = bitarray()
        bit_array.frombytes(bytes)
        raw_civilian_entity_id = cls.read_with_exist_flag(
            bit_array, cls.SIZE_CIVILIAN_ENTITY_ID
        )
        civilian_entity_id = (
            EntityID(raw_civilian_entity_id) if raw_civilian_entity_id else None
        )
        civilian_hp = cls.read_with_exist_flag(bit_array, cls.SIZE_CIVILIAN_HP)
        civilian_buriedness = cls.read_with_exist_flag(
            bit_array, cls.SIZE_CIVILIAN_BURIEDNESS
        )
        civilian_damage = cls.read_with_exist_flag(bit_array, cls.SIZE_CIVILIAN_DAMAGE)
        raw_civilian_position = cls.read_with_exist_flag(
            bit_array, cls.SIZE_CIVILIAN_POSITION
        )
        civilian_position = (
            EntityID(raw_civilian_position) if raw_civilian_position else None
        )
        civilian = Civilian(
            civilian_entity_id.get_value() if civilian_entity_id else None
        )
        civilian.set_hp(civilian_hp)
        civilian.set_buriedness(civilian_buriedness)
        civilian.set_damage(civilian_damage)
        civilian.set_position(civilian_position)
        return MessageCivilian(
            False,
            civilian,
        )

    def get_check_key(self) -> str:
        civilian_entity_id_value = (
            self._civilian_entity_id.get_value() if self._civilian_entity_id else None
        )
        return f"{self.__class__.__name__} > civilian: {civilian_entity_id_value}"

    def get_civilian_entity_id(self) -> Optional[EntityID]:
        return self._civilian_entity_id

    def get_civilian_hp(self) -> Optional[int]:
        return self._civilian_hp

    def get_civilian_buriedness(self) -> Optional[int]:
        return self._civilian_buriedness

    def get_civilian_damage(self) -> Optional[int]:
        return self._civilian_damage

    def get_civilian_position(self) -> Optional[EntityID]:
        return self._civilian_position
