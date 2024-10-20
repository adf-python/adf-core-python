from __future__ import annotations

from typing import Optional

from bitarray import bitarray
from rcrs_core.entities.policeForce import PoliceForceEntity
from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.communication.standard.bundle.standard_message import (
    StandardMessage,
)
from adf_core_python.core.agent.communication.standard.bundle.standard_message_priority import (
    StandardMessagePriority,
)


class MessagePoliceForce(StandardMessage):
    CTION_REST: int = 0
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
        police_force: PoliceForceEntity,
        action: int,
        target_entity_id: EntityID,
        priority: StandardMessagePriority = StandardMessagePriority.NORMAL,
        sender_id: int = -1,
        ttl: int = -1,
    ):
        super().__init__(is_wireless_message, priority, sender_id, ttl)
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

    def get_byte_size(self) -> int:
        return self.to_bytes().__len__()

    def to_bytes(self) -> bytes:
        bit_array = bitarray()
        self.write_with_exist_flag(
            bit_array,
            self._police_force_entity_id.get_value()
            if self._police_force_entity_id
            else None,
            self.SIZE_POLICE_FORCE_ENTITY_ID,
        )
        self.write_with_exist_flag(
            bit_array,
            self._police_force_hp,
            self.SIZE_POLICE_FORCE_HP,
        )
        self.write_with_exist_flag(
            bit_array,
            self._police_force_buriedness,
            self.SIZE_POLICE_FORCE_BURIEDNESS,
        )
        self.write_with_exist_flag(
            bit_array,
            self._police_force_damage,
            self.SIZE_POLICE_FORCE_DAMAGE,
        )
        self.write_with_exist_flag(
            bit_array,
            self._police_force_position.get_value()
            if self._police_force_position
            else None,
            self.SIZE_POLICE_FORCE_POSITION,
        )
        self.write_with_exist_flag(
            bit_array,
            self._target_entity_id.get_value() if self._target_entity_id else None,
            self.SIZE_TARGET_ENTITY_ID,
        )
        self.write_with_exist_flag(bit_array, self._action, self.SIZE_ACTION)
        return bit_array.tobytes()

    @classmethod
    def from_bytes(cls, bytes: bytes) -> MessagePoliceForce:
        bit_array = bitarray()
        bit_array.frombytes(bytes)
        raw_police_force_entity_id = cls.read_with_exist_flag(
            bit_array, cls.SIZE_POLICE_FORCE_ENTITY_ID
        )
        police_force_entity_id = (
            EntityID(raw_police_force_entity_id) if raw_police_force_entity_id else None
        )
        police_force_hp = cls.read_with_exist_flag(bit_array, cls.SIZE_POLICE_FORCE_HP)
        police_force_buriedness = cls.read_with_exist_flag(
            bit_array, cls.SIZE_POLICE_FORCE_BURIEDNESS
        )
        police_force_damage = cls.read_with_exist_flag(
            bit_array, cls.SIZE_POLICE_FORCE_DAMAGE
        )
        raw_police_force_position = cls.read_with_exist_flag(
            bit_array, cls.SIZE_POLICE_FORCE_POSITION
        )
        police_force_position = (
            EntityID(raw_police_force_position) if raw_police_force_position else None
        )
        raw_target_entity_id = cls.read_with_exist_flag(
            bit_array, cls.SIZE_TARGET_ENTITY_ID
        )
        target_entity_id = (
            EntityID(raw_target_entity_id) if raw_target_entity_id else None
        )
        action = cls.read_with_exist_flag(bit_array, cls.SIZE_ACTION)
        police_force = PoliceForceEntity(
            police_force_entity_id.get_value() if police_force_entity_id else None
        )
        police_force.set_hp(police_force_hp)
        police_force.set_buriedness(police_force_buriedness)
        police_force.set_damage(police_force_damage)
        police_force.set_position(police_force_position)
        return MessagePoliceForce(
            False,
            police_force,
            action or -1,
            target_entity_id or EntityID(-1),
        )

    def get_check_key(self) -> str:
        police_force_entity_id_value = (
            self._police_force_entity_id.get_value()
            if self._police_force_entity_id
            else None
        )
        target_entity_id_value = (
            self._target_entity_id.get_value() if self._target_entity_id else None
        )
        return f"{self.__class__.__name__} > police force: {police_force_entity_id_value} > target: {target_entity_id_value} > action: {self._action}"

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
