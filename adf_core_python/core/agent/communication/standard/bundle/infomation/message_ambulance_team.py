from typing import TYPE_CHECKING, Optional

from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.communication.standard.bundle.standard_message import (
    StandardMessage,
)
from adf_core_python.core.agent.communication.standard.bundle.standard_message_priority import (
    StandardMessagePriority,
)

if TYPE_CHECKING:
    from rcrs_core.entities.ambulanceTeam import AmbulanceTeamEntity


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
        sender_id: int,
        ttl: int,
        priority: StandardMessagePriority,
        ambulance_team: AmbulanceTeamEntity,
        action: int,
        target_entity_id: EntityID,
    ):
        super().__init__(is_wireless_message, sender_id, ttl, priority)
        self._ambulance_team_entity_id: Optional[EntityID] = ambulance_team.get_id()
        self._ambulance_team_hp: Optional[int] = ambulance_team.get_hp() or -1
        self._ambulance_team_buriedness: Optional[int] = (
            ambulance_team.get_buriedness() or -1
        )
        self._ambulance_team_damage: Optional[int] = ambulance_team.get_damage() or -1
        self._ambulance_team_position: Optional[EntityID] = (
            ambulance_team.get_position() or EntityID(-1)
        )
        self._target_entity_id: Optional[EntityID] = target_entity_id
        self._action: Optional[int] = action

    def get_byte_size(self) -> int:
        return self.to_bytes().__len__()

    def to_bytes(self) -> bytes:
        byte_array = bytearray()
        self.write_with_exist_flag(
            byte_array,
            self._ambulance_team_entity_id.get_value()
            if self._ambulance_team_entity_id
            else None,
            self.SIZE_AMBULANCE_TEAM_ENTITY_ID,
        )
        self.write_with_exist_flag(
            byte_array, self._ambulance_team_hp, self.SIZE_AMBULANCE_TEAM_HP
        )
        self.write_with_exist_flag(
            byte_array,
            self._ambulance_team_buriedness,
            self.SIZE_AMBULANCE_TEAM_BURIEDNESS,
        )
        self.write_with_exist_flag(
            byte_array, self._ambulance_team_damage, self.SIZE_AMBULANCE_TEAM_DAMAGE
        )
        self.write_with_exist_flag(
            byte_array,
            self._ambulance_team_position.get_value()
            if self._ambulance_team_position
            else None,
            self.SIZE_AMBULANCE_TEAM_POSITION,
        )
        self.write_with_exist_flag(
            byte_array,
            self._target_entity_id.get_value() if self._target_entity_id else None,
            self.SIZE_TARGET_ENTITY_ID,
        )
        self.write_with_exist_flag(byte_array, self._action, self.SIZE_ACTION)
        return bytes(byte_array)

    def from_bytes(self, bytes: bytes) -> None:
        byte_array = bytearray(bytes)
        raw_ambulance_team_entity_id = self.read_with_exist_flag(
            byte_array, self.SIZE_AMBULANCE_TEAM_ENTITY_ID
        )
        self._ambulance_team_entity_id = (
            EntityID(raw_ambulance_team_entity_id)
            if raw_ambulance_team_entity_id
            else None
        )
        self._ambulance_team_hp = self.read_with_exist_flag(
            byte_array, self.SIZE_AMBULANCE_TEAM_HP
        )
        self._ambulance_team_buriedness = self.read_with_exist_flag(
            byte_array, self.SIZE_AMBULANCE_TEAM_BURIEDNESS
        )
        self._ambulance_team_damage = self.read_with_exist_flag(
            byte_array, self.SIZE_AMBULANCE_TEAM_DAMAGE
        )
        raw_ambulance_team_position = self.read_with_exist_flag(
            byte_array, self.SIZE_AMBULANCE_TEAM_POSITION
        )
        self._ambulance_team_position = (
            EntityID(raw_ambulance_team_position)
            if raw_ambulance_team_position
            else None
        )
        raw_target_entity_id = self.read_with_exist_flag(
            byte_array, self.SIZE_TARGET_ENTITY_ID
        )
        self._target_entity_id = (
            EntityID(raw_target_entity_id) if raw_target_entity_id else None
        )
        self._action = self.read_with_exist_flag(byte_array, self.SIZE_ACTION)

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
