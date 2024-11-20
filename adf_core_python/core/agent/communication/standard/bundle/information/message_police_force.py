from __future__ import annotations

from typing import Optional

from bitarray import bitarray
from rcrs_core.entities.policeForce import PoliceForce
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


class MessagePoliceForce(StandardMessage):
    ACTION_REST: int = 0
    ACTION_MOVE: int = 1
    ACTION_CLEAR: int = 2

    SIZE_POLICE_FORCE_ENTITY_ID: int = 32
    SIZE_POLICE_FORCE_HP: int = 14
    SIZE_POLICE_FORCE_BURIEDNESS: int = 13
    SIZE_POLICE_FORCE_DAMAGE: int = 14
    SIZE_POLICE_FORCE_POSITION: int = 32
    SIZE_TARGET_ENTITY_ID: int = 32
    SIZE_ACTION: int = 4

    def __init__(
        self,
        is_wireless_message: bool,
        police_force: PoliceForce,
        action: int,
        target_entity_id: EntityID,
        priority: StandardMessagePriority,
        sender_entity_id: EntityID,
        ttl: Optional[int] = None,
    ):
        super().__init__(is_wireless_message, priority, sender_entity_id, ttl)
        self._police_force_entity_id: Optional[EntityID] = police_force.get_id()
        self._police_force_hp: Optional[int] = police_force.get_hp() or None
        self._police_force_buriedness: Optional[int] = (
            police_force.get_buriedness() or None
        )
        self._police_force_damage: Optional[int] = police_force.get_damage() or None
        self._police_force_position: Optional[EntityID] = (
            police_force.get_position() or None
        )
        self._target_entity_id: Optional[EntityID] = target_entity_id
        self._action: Optional[int] = action

    def get_police_force_entity_id(self) -> Optional[EntityID]:
        return self._police_force_entity_id

    def get_police_force_hp(self) -> Optional[int]:
        return self._police_force_hp

    def get_police_force_buriedness(self) -> Optional[int]:
        return self._police_force_buriedness

    def get_police_force_damage(self) -> Optional[int]:
        return self._police_force_damage

    def get_police_force_position(self) -> Optional[EntityID]:
        return self._police_force_position

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
            self._police_force_entity_id.get_value()
            if self._police_force_entity_id
            else None,
            self.SIZE_POLICE_FORCE_ENTITY_ID,
        )
        write_with_exist_flag(
            bit_array,
            self._police_force_hp,
            self.SIZE_POLICE_FORCE_HP,
        )
        write_with_exist_flag(
            bit_array,
            self._police_force_buriedness,
            self.SIZE_POLICE_FORCE_BURIEDNESS,
        )
        write_with_exist_flag(
            bit_array,
            self._police_force_damage,
            self.SIZE_POLICE_FORCE_DAMAGE,
        )
        write_with_exist_flag(
            bit_array,
            self._police_force_position.get_value()
            if self._police_force_position
            else None,
            self.SIZE_POLICE_FORCE_POSITION,
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
    ) -> MessagePoliceForce:
        std_message = super().from_bits(
            bit_array, is_wireless_message, sender_entity_id
        )
        police_force_id = read_with_exist_flag(
            bit_array, cls.SIZE_POLICE_FORCE_ENTITY_ID
        )
        police_force_hp = read_with_exist_flag(bit_array, cls.SIZE_POLICE_FORCE_HP)
        police_force_buriedness = read_with_exist_flag(
            bit_array, cls.SIZE_POLICE_FORCE_BURIEDNESS
        )
        police_force_damage = read_with_exist_flag(
            bit_array, cls.SIZE_POLICE_FORCE_DAMAGE
        )
        raw_police_force_position = read_with_exist_flag(
            bit_array, cls.SIZE_POLICE_FORCE_POSITION
        )
        police_force_position = (
            EntityID(raw_police_force_position) if raw_police_force_position else None
        )
        raw_target_entity_id = read_with_exist_flag(
            bit_array, cls.SIZE_TARGET_ENTITY_ID
        )
        target_entity_id = (
            EntityID(raw_target_entity_id) if raw_target_entity_id else EntityID(-1)
        )
        action = read_with_exist_flag(bit_array, cls.SIZE_ACTION)
        police_force = PoliceForce(police_force_id or -1)
        police_force.set_hp(police_force_hp)
        police_force.set_buriedness(police_force_buriedness)
        police_force.set_damage(police_force_damage)
        police_force.set_position(police_force_position)
        return MessagePoliceForce(
            False,
            police_force,
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
                self._police_force_entity_id,
                self._police_force_hp,
                self._police_force_buriedness,
                self._police_force_damage,
                self._police_force_position,
                self._target_entity_id,
                self._action,
            )
        )

    def __str__(self) -> str:
        return f"MessagePoliceForce(police_force_entity_id={self._police_force_entity_id}, police_force_hp={self._police_force_hp}, police_force_buriedness={self._police_force_buriedness}, police_force_damage={self._police_force_damage}, police_force_position={self._police_force_position}, target_entity_id={self._target_entity_id}, action={self._action})"
