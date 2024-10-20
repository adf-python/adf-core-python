from __future__ import annotations

from typing import Optional

from bitarray import bitarray
from rcrs_core.entities.fireBrigade import FireBrigadeEntity
from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.communication.standard.bundle.standard_message import (
    StandardMessage,
)
from adf_core_python.core.agent.communication.standard.bundle.standard_message_priority import (
    StandardMessagePriority,
)


class MessageFireBrigade(StandardMessage):
    CTION_REST: int = 0
    ACTION_MOVE: int = 1
    ACTION_EXTINGUISH: int = 2
    ACTION_REFILL: int = 3
    ACTION_RESCUE: int = 4

    SIZE_FIRE_BRIGADE_ENTITY_ID: int = 32
    SIZE_FIRE_BRIGADE_HP: int = 14
    SIZE_FIRE_BRIGADE_BURIEDNESS: int = 13
    SIZE_FIRE_BRIGADE_DAMAGE: int = 14
    SIZE_FIRE_BRIGADE_POSITION: int = 32
    SIZE_FIRE_BRIGADE_WATER: int = 14
    SIZE_TARGET_ENTITY_ID: int = 32
    SIZE_ACTION: int = 4

    def __init__(
        self,
        is_wireless_message: bool,
        fire_brigade: FireBrigadeEntity,
        action: int,
        target_entity_id: EntityID,
        priority: StandardMessagePriority = StandardMessagePriority.NORMAL,
        sender_id: int = -1,
        ttl: int = -1,
    ):
        super().__init__(is_wireless_message, priority, sender_id, ttl)
        self._fire_brigade_entity_id: Optional[EntityID] = fire_brigade.get_id()
        self._fire_brigade_hp: Optional[int] = fire_brigade.get_hp() or None
        self._fire_brigade_buriedness: Optional[int] = (
            fire_brigade.get_buriedness() or None
        )
        self._fire_brigade_damage: Optional[int] = fire_brigade.get_damage() or None
        self._fire_brigade_position: Optional[EntityID] = (
            fire_brigade.get_position() or None
        )
        self._fire_brigade_water: Optional[int] = fire_brigade.get_water() or None
        self._target_entity_id: Optional[EntityID] = target_entity_id
        self._action: Optional[int] = action

    def get_byte_size(self) -> int:
        return self.to_bytes().__len__()

    def to_bytes(self) -> bytes:
        bit_array = bitarray()
        self.write_with_exist_flag(
            bit_array,
            self._fire_brigade_entity_id.get_value()
            if self._fire_brigade_entity_id
            else None,
            self.SIZE_FIRE_BRIGADE_ENTITY_ID,
        )
        self.write_with_exist_flag(
            bit_array,
            self._fire_brigade_hp,
            self.SIZE_FIRE_BRIGADE_HP,
        )
        self.write_with_exist_flag(
            bit_array,
            self._fire_brigade_buriedness,
            self.SIZE_FIRE_BRIGADE_BURIEDNESS,
        )
        self.write_with_exist_flag(
            bit_array,
            self._fire_brigade_damage,
            self.SIZE_FIRE_BRIGADE_DAMAGE,
        )
        self.write_with_exist_flag(
            bit_array,
            self._fire_brigade_position.get_value()
            if self._fire_brigade_position
            else None,
            self.SIZE_FIRE_BRIGADE_POSITION,
        )
        self.write_with_exist_flag(
            bit_array,
            self._fire_brigade_water,
            self.SIZE_FIRE_BRIGADE_WATER,
        )
        self.write_with_exist_flag(
            bit_array,
            self._target_entity_id.get_value() if self._target_entity_id else None,
            self.SIZE_TARGET_ENTITY_ID,
        )
        self.write_with_exist_flag(bit_array, self._action, self.SIZE_ACTION)
        return bit_array.tobytes()

    @classmethod
    def from_bytes(cls, bytes: bytes) -> MessageFireBrigade:
        bit_array = bitarray()
        bit_array.frombytes(bytes)
        raw_fire_brigade_entity_id = cls.read_with_exist_flag(
            bit_array, cls.SIZE_FIRE_BRIGADE_ENTITY_ID
        )
        fire_brigade_entity_id = (
            EntityID(raw_fire_brigade_entity_id) if raw_fire_brigade_entity_id else None
        )
        fire_brigade_hp = cls.read_with_exist_flag(bit_array, cls.SIZE_FIRE_BRIGADE_HP)
        fire_brigade_buriedness = cls.read_with_exist_flag(
            bit_array, cls.SIZE_FIRE_BRIGADE_BURIEDNESS
        )
        fire_brigade_damage = cls.read_with_exist_flag(
            bit_array, cls.SIZE_FIRE_BRIGADE_DAMAGE
        )
        raw_fire_brigade_position = cls.read_with_exist_flag(
            bit_array, cls.SIZE_FIRE_BRIGADE_POSITION
        )
        fire_brigade_position = (
            EntityID(raw_fire_brigade_position) if raw_fire_brigade_position else None
        )
        fire_brigade_water = cls.read_with_exist_flag(
            bit_array, cls.SIZE_FIRE_BRIGADE_WATER
        )
        raw_target_entity_id = cls.read_with_exist_flag(
            bit_array, cls.SIZE_TARGET_ENTITY_ID
        )
        target_entity_id = (
            EntityID(raw_target_entity_id) if raw_target_entity_id else None
        )
        action = cls.read_with_exist_flag(bit_array, cls.SIZE_ACTION)
        fire_brigade = FireBrigadeEntity(
            fire_brigade_entity_id.get_value() if fire_brigade_entity_id else None
        )
        fire_brigade.set_hp(fire_brigade_hp)
        fire_brigade.set_buriedness(fire_brigade_buriedness)
        fire_brigade.set_damage(fire_brigade_damage)
        fire_brigade.set_position(fire_brigade_position)
        fire_brigade.set_water(fire_brigade_water)
        return MessageFireBrigade(
            False,
            fire_brigade,
            action or -1,
            target_entity_id or EntityID(-1),
        )

    def get_check_key(self) -> str:
        fire_brigade_entity_id_value = (
            self._fire_brigade_entity_id.get_value()
            if self._fire_brigade_entity_id
            else None
        )
        target_entity_id_value = (
            self._target_entity_id.get_value() if self._target_entity_id else None
        )
        return f"{self.__class__.__name__} > fire brigade: {fire_brigade_entity_id_value} > target: {target_entity_id_value} > action: {self._action}"

    def get_fire_brigade_entity_id(self) -> Optional[EntityID]:
        return self._fire_brigade_entity_id

    def get_fire_brigade_hp(self) -> Optional[int]:
        return self._fire_brigade_hp

    def get_fire_brigade_buriedness(self) -> Optional[int]:
        return self._fire_brigade_buriedness

    def get_fire_brigade_damage(self) -> Optional[int]:
        return self._fire_brigade_damage

    def get_fire_brigade_position(self) -> Optional[EntityID]:
        return self._fire_brigade_position

    def get_fire_brigade_water(self) -> Optional[int]:
        return self._fire_brigade_water

    def get_target_entity_id(self) -> Optional[EntityID]:
        return self._target_entity_id

    def get_action(self) -> Optional[int]:
        return self._action
