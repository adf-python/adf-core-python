from __future__ import annotations

from typing import Optional

from bitarray import bitarray
from rcrscore.entities import AmbulanceTeam, EntityID

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
    ambulance_team: AmbulanceTeam,
    action: int,
    target_entity_id: EntityID,
    priority: StandardMessagePriority,
    sender_entity_id: EntityID,
    ttl: Optional[int] = None,
  ):
    super().__init__(is_wireless_message, priority, sender_entity_id, ttl)
    self._ambulance_team_entity_id: Optional[EntityID] = ambulance_team.get_entity_id()
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

  def get_bit_size(self) -> int:
    return self.to_bits().__len__()

  def to_bits(self) -> bitarray:
    bit_array = super().to_bits()
    write_with_exist_flag(
      bit_array,
      self._ambulance_team_entity_id.get_value()
      if self._ambulance_team_entity_id
      else None,
      self.SIZE_AMBULANCE_TEAM_ENTITY_ID,
    )
    write_with_exist_flag(
      bit_array, self._ambulance_team_hp, self.SIZE_AMBULANCE_TEAM_HP
    )
    write_with_exist_flag(
      bit_array,
      self._ambulance_team_buriedness,
      self.SIZE_AMBULANCE_TEAM_BURIEDNESS,
    )
    write_with_exist_flag(
      bit_array, self._ambulance_team_damage, self.SIZE_AMBULANCE_TEAM_DAMAGE
    )
    write_with_exist_flag(
      bit_array,
      self._ambulance_team_position.get_value()
      if self._ambulance_team_position
      else None,
      self.SIZE_AMBULANCE_TEAM_POSITION,
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
    cls,
    bit_array: bitarray,
    is_wireless_message: bool,
    sender_entity_id: EntityID,
  ) -> MessageAmbulanceTeam:
    std_message = super().from_bits(bit_array, is_wireless_message, sender_entity_id)
    ambulance_team_id = read_with_exist_flag(
      bit_array, cls.SIZE_AMBULANCE_TEAM_ENTITY_ID
    )
    ambulance_team_hp = read_with_exist_flag(bit_array, cls.SIZE_AMBULANCE_TEAM_HP)
    ambulance_team_buriedness = read_with_exist_flag(
      bit_array, cls.SIZE_AMBULANCE_TEAM_BURIEDNESS
    )
    ambulance_team_damage = read_with_exist_flag(
      bit_array, cls.SIZE_AMBULANCE_TEAM_DAMAGE
    )
    raw_ambulance_team_position = read_with_exist_flag(
      bit_array, cls.SIZE_AMBULANCE_TEAM_POSITION
    )
    ambulance_team_position = (
      EntityID(raw_ambulance_team_position)
      if raw_ambulance_team_position is not None
      else None
    )
    raw_target_entity_id = read_with_exist_flag(bit_array, cls.SIZE_TARGET_ENTITY_ID)
    target_entity_id = (
      EntityID(raw_target_entity_id)
      if raw_target_entity_id is not None
      else EntityID(-1)
    )
    action = read_with_exist_flag(bit_array, cls.SIZE_ACTION)
    ambulance_team = AmbulanceTeam(ambulance_team_id or -1)
    ambulance_team.set_hp(ambulance_team_hp)
    ambulance_team.set_buriedness(ambulance_team_buriedness)
    ambulance_team.set_damage(ambulance_team_damage)
    ambulance_team.set_position(ambulance_team_position)
    return MessageAmbulanceTeam(
      False,
      ambulance_team,
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
        self._ambulance_team_entity_id,
        self._ambulance_team_hp,
        self._ambulance_team_buriedness,
        self._ambulance_team_damage,
        self._ambulance_team_position,
        self._target_entity_id,
        self._action,
      )
    )

  def __str__(self) -> str:
    return f"MessageAmbulanceTeam(ambulance_team_entity_id={self._ambulance_team_entity_id}, ambulance_team_hp={self._ambulance_team_hp}, ambulance_team_buriedness={self._ambulance_team_buriedness}, ambulance_team_damage={self._ambulance_team_damage}, ambulance_team_position={self._ambulance_team_position}, target_entity_id={self._target_entity_id}, action={self._action}, ttl={self._ttl})"
