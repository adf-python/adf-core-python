from __future__ import annotations

from typing import Optional

from bitarray import bitarray
from rcrs_core.entities.fireBrigade import FireBrigade
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


class MessageFireBrigade(StandardMessage):
    ACTION_REST: int = 0
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
        fire_brigade: FireBrigade,
        action: int,
        target_entity_id: EntityID,
        priority: StandardMessagePriority,
        sender_entity_id: EntityID,
        ttl: Optional[int] = None,
    ):
        super().__init__(is_wireless_message, priority, sender_entity_id, ttl)
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

    def get_bit_size(self) -> int:
        return self.to_bits().__len__()

    def to_bits(self) -> bitarray:
        bit_array = super().to_bits()
        write_with_exist_flag(
            bit_array,
            self._fire_brigade_entity_id.get_value()
            if self._fire_brigade_entity_id
            else None,
            self.SIZE_FIRE_BRIGADE_ENTITY_ID,
        )
        write_with_exist_flag(
            bit_array,
            self._fire_brigade_hp,
            self.SIZE_FIRE_BRIGADE_HP,
        )
        write_with_exist_flag(
            bit_array,
            self._fire_brigade_buriedness,
            self.SIZE_FIRE_BRIGADE_BURIEDNESS,
        )
        write_with_exist_flag(
            bit_array,
            self._fire_brigade_damage,
            self.SIZE_FIRE_BRIGADE_DAMAGE,
        )
        write_with_exist_flag(
            bit_array,
            self._fire_brigade_position.get_value()
            if self._fire_brigade_position
            else None,
            self.SIZE_FIRE_BRIGADE_POSITION,
        )
        write_with_exist_flag(
            bit_array,
            self._fire_brigade_water,
            self.SIZE_FIRE_BRIGADE_WATER,
        )
        write_with_exist_flag(
            bit_array,
            self._target_entity_id.get_value() if self._target_entity_id else None,
            self.SIZE_TARGET_ENTITY_ID,
        )
        write_with_exist_flag(bit_array, self._action, self.SIZE_ACTION)
        return bit_array

    @classmethod
    def from_bits(
        cls, bit_array: bitarray, is_wireless_message: bool, sender_entity_id: EntityID
    ) -> MessageFireBrigade:
        std_message = super().from_bits(
            bit_array, is_wireless_message, sender_entity_id
        )
        fire_brigade_id = read_with_exist_flag(
            bit_array, cls.SIZE_FIRE_BRIGADE_ENTITY_ID
        )
        fire_brigade_hp = read_with_exist_flag(bit_array, cls.SIZE_FIRE_BRIGADE_HP)
        fire_brigade_buriedness = read_with_exist_flag(
            bit_array, cls.SIZE_FIRE_BRIGADE_BURIEDNESS
        )
        fire_brigade_damage = read_with_exist_flag(
            bit_array, cls.SIZE_FIRE_BRIGADE_DAMAGE
        )
        raw_fire_brigade_position = read_with_exist_flag(
            bit_array, cls.SIZE_FIRE_BRIGADE_POSITION
        )
        fire_brigade_position = (
            EntityID(raw_fire_brigade_position) if raw_fire_brigade_position else None
        )
        fire_brigade_water = read_with_exist_flag(
            bit_array, cls.SIZE_FIRE_BRIGADE_WATER
        )
        raw_target_entity_id = read_with_exist_flag(
            bit_array, cls.SIZE_TARGET_ENTITY_ID
        )
        target_entity_id = (
            EntityID(raw_target_entity_id) if raw_target_entity_id else EntityID(-1)
        )
        action = read_with_exist_flag(bit_array, cls.SIZE_ACTION)
        fire_brigade = FireBrigade(
            fire_brigade_id or -1,
        )
        fire_brigade.set_hp(fire_brigade_hp)
        fire_brigade.set_buriedness(fire_brigade_buriedness)
        fire_brigade.set_damage(fire_brigade_damage)
        fire_brigade.set_position(fire_brigade_position)
        fire_brigade.set_water(fire_brigade_water)
        return MessageFireBrigade(
            False,
            fire_brigade,
            action if action is not None else -1,
            target_entity_id,
            StandardMessagePriority.NORMAL,
            sender_entity_id,
            std_message.get_ttl(),
        )

    def __hash__(self) -> int:
        h = super().__hash__()
        return hash(
            (
                h,
                self._fire_brigade_entity_id,
                self._fire_brigade_hp,
                self._fire_brigade_buriedness,
                self._fire_brigade_damage,
                self._fire_brigade_position,
                self._fire_brigade_water,
                self._target_entity_id,
                self._action,
            )
        )

    def __str__(self) -> str:
        return f"MessageFireBrigade(fire_brigade_entity_id={self._fire_brigade_entity_id}, fire_brigade_hp={self._fire_brigade_hp}, fire_brigade_buriedness={self._fire_brigade_buriedness}, fire_brigade_damage={self._fire_brigade_damage}, fire_brigade_position={self._fire_brigade_position}, fire_brigade_water={self._fire_brigade_water}, target_entity_id={self._target_entity_id}, action={self._action})"
