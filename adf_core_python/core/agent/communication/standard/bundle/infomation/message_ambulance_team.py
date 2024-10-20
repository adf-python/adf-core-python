from __future__ import annotations

from typing import Optional

from bitarray import bitarray
from rcrs_core.entities.ambulanceTeam import AmbulanceTeamEntity
from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.communication.standard.bundle.standard_message import (
    StandardMessage,
)
from adf_core_python.core.agent.communication.standard.bundle.standard_message_priority import (
    StandardMessagePriority,
)


class MessageAmbulanceTeam(StandardMessage):
    ACTION_REST: int = 0
    ACTION_MOVE: int = 1
    ACTION_RESCUE: int = 2
    ACTION_LOAD: int = 3
    ACTION_UNLOAD: int = 4

    SIZE_AMBULANCE_TEAM_ENTITY_ID: int = 32
    SIZE_AMBULANCE_TEAM_HP: int = 14
    SIZE_AMBULANCE_TEAM_BURIEDNESS: int = 13
    SIZE_AMBULANCE_TEAM_DAMAGE: int = 14
    SIZE_AMBULANCE_TEAM_POSITION: int = 32
    SIZE_TARGET_ENTITY_ID: int = 32
    SIZE_ACTION: int = 4

    def __init__(
        self,
        is_wireless_message: bool,
        priority: StandardMessagePriority,
        ambulance_team: AmbulanceTeamEntity,
        action: int,
        target_entity_id: EntityID,
        sender_id: int = -1,
        ttl: int = -1,
    ):
        super().__init__(is_wireless_message, priority, sender_id, ttl)
        self._ambulance_team_entity_id: Optional[EntityID] = ambulance_team.get_id()
        self._ambulance_team_hp: Optional[int] = ambulance_team.get_hp() or None
        self._ambulance_team_buriedness: Optional[int] = (
            ambulance_team.get_buriedness() or None
        )
        self._ambulance_team_damage: Optional[int] = ambulance_team.get_damage() or None
        self._ambulance_team_position: Optional[EntityID] = (
            ambulance_team.get_position() or None
        )
        self._target_entity_id: Optional[EntityID] = target_entity_id
        self._action: Optional[int] = action

    def get_byte_size(self) -> int:
        return self.to_bytes().__len__()

    def to_bytes(self) -> bytes:
        bit_array = bitarray()
        self.write_with_exist_flag(
            bit_array,
            self._ambulance_team_entity_id.get_value()
            if self._ambulance_team_entity_id
            else None,
            self.SIZE_AMBULANCE_TEAM_ENTITY_ID,
        )
        self.write_with_exist_flag(
            bit_array, self._ambulance_team_hp, self.SIZE_AMBULANCE_TEAM_HP
        )
        self.write_with_exist_flag(
            bit_array,
            self._ambulance_team_buriedness,
            self.SIZE_AMBULANCE_TEAM_BURIEDNESS,
        )
        self.write_with_exist_flag(
            bit_array, self._ambulance_team_damage, self.SIZE_AMBULANCE_TEAM_DAMAGE
        )
        self.write_with_exist_flag(
            bit_array,
            self._ambulance_team_position.get_value()
            if self._ambulance_team_position
            else None,
            self.SIZE_AMBULANCE_TEAM_POSITION,
        )
        self.write_with_exist_flag(
            bit_array,
            self._target_entity_id.get_value() if self._target_entity_id else None,
            self.SIZE_TARGET_ENTITY_ID,
        )
        self.write_with_exist_flag(bit_array, self._action, self.SIZE_ACTION)
        return bit_array.tobytes()

    @classmethod
    def from_bytes(cls, bytes: bytes) -> MessageAmbulanceTeam:
        bit_array = bitarray()
        bit_array.frombytes(bytes)
        raw_ambulance_team_entity_id = cls.read_with_exist_flag(
            bit_array, cls.SIZE_AMBULANCE_TEAM_ENTITY_ID
        )
        ambulance_team_entity_id = (
            EntityID(raw_ambulance_team_entity_id)
            if raw_ambulance_team_entity_id is not None
            else None
        )
        ambulance_team_hp = cls.read_with_exist_flag(
            bit_array, cls.SIZE_AMBULANCE_TEAM_HP
        )
        ambulance_team_buriedness = cls.read_with_exist_flag(
            bit_array, cls.SIZE_AMBULANCE_TEAM_BURIEDNESS
        )
        ambulance_team_damage = cls.read_with_exist_flag(
            bit_array, cls.SIZE_AMBULANCE_TEAM_DAMAGE
        )

        raw_ambulance_team_position = cls.read_with_exist_flag(
            bit_array, cls.SIZE_AMBULANCE_TEAM_POSITION
        )
        ambulance_team_position = (
            EntityID(raw_ambulance_team_position)
            if raw_ambulance_team_position is not None
            else None
        )

        raw_target_entity_id = cls.read_with_exist_flag(
            bit_array, cls.SIZE_TARGET_ENTITY_ID
        )
        target_entity_id = (
            EntityID(raw_target_entity_id) if raw_target_entity_id is not None else None
        )
        action = cls.read_with_exist_flag(bit_array, cls.SIZE_ACTION)
        ambulance_team = AmbulanceTeamEntity(
            ambulance_team_entity_id,
        )
        ambulance_team.set_hp(ambulance_team_hp)
        ambulance_team.set_buriedness(ambulance_team_buriedness)
        ambulance_team.set_damage(ambulance_team_damage)
        ambulance_team.set_position(ambulance_team_position)
        return MessageAmbulanceTeam(
            False,
            StandardMessagePriority.NORMAL,
            ambulance_team,
            action or -1,
            target_entity_id or EntityID(-1),
        )

    def get_check_key(self) -> str:
        target_id_value: str = (
            str(self._target_entity_id.get_value())
            if self._target_entity_id
            else "None"
        )
        ambulance_team_id_value: str = (
            str(self._ambulance_team_entity_id.get_value())
            if self._ambulance_team_entity_id
            else "None"
        )
        return f"{self.__class__.__name__} > agent: {ambulance_team_id_value}, target: {target_id_value}, action: {self._action}"

    def get_ambulance_team_entity_id(self) -> Optional[EntityID]:
        return self._ambulance_team_entity_id

    def get_ambulance_team_hp(self) -> Optional[int]:
        return self._ambulance_team_hp

    def get_ambulance_team_buriedness(self) -> Optional[int]:
        return self._ambulance_team_buriedness

    def get_ambulance_team_damage(self) -> Optional[int]:
        return self._ambulance_team_damage

    def get_ambulance_team_position(self) -> Optional[EntityID]:
        return self._ambulance_team_position

    def get_target_entity_id(self) -> Optional[EntityID]:
        return self._target_entity_id

    def get_action(self) -> Optional[int]:
        return self._action
