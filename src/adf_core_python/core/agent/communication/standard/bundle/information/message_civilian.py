from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from rcrscore.entities import EntityID
from rcrscore.entities.civilian import Civilian

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

if TYPE_CHECKING:
  from bitarray import bitarray


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
    priority: StandardMessagePriority,
    sender_entity_id: EntityID,
    ttl: Optional[int] = None,
  ):
    super().__init__(is_wireless_message, priority, sender_entity_id, ttl)
    self._civilian_entity_id: Optional[EntityID] = civilian.get_entity_id()
    self._civilian_hp: Optional[int] = civilian.get_hp() or None
    self._civilian_buriedness: Optional[int] = civilian.get_buriedness() or None
    self._civilian_damage: Optional[int] = civilian.get_damage() or None
    self._civilian_position: Optional[EntityID] = civilian.get_position() or None

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

  def get_bit_size(self) -> int:
    return self.to_bits().__len__()

  def to_bits(self) -> bitarray:
    bit_array = super().to_bits()
    write_with_exist_flag(
      bit_array,
      self._civilian_entity_id.get_value() if self._civilian_entity_id else None,
      self.SIZE_CIVILIAN_ENTITY_ID,
    )
    write_with_exist_flag(
      bit_array,
      self._civilian_hp,
      self.SIZE_CIVILIAN_HP,
    )
    write_with_exist_flag(
      bit_array,
      self._civilian_buriedness,
      self.SIZE_CIVILIAN_BURIEDNESS,
    )
    write_with_exist_flag(
      bit_array,
      self._civilian_damage,
      self.SIZE_CIVILIAN_DAMAGE,
    )
    write_with_exist_flag(
      bit_array,
      self._civilian_position.get_value() if self._civilian_position else None,
      self.SIZE_CIVILIAN_POSITION,
    )
    return bit_array

  @classmethod
  def from_bits(
    cls, bit_array: bitarray, is_wireless_message: bool, sender_entity_id: EntityID
  ) -> MessageCivilian:
    std_message = super().from_bits(bit_array, is_wireless_message, sender_entity_id)
    civilian_id = read_with_exist_flag(bit_array, cls.SIZE_CIVILIAN_ENTITY_ID)
    civilian_hp = read_with_exist_flag(bit_array, cls.SIZE_CIVILIAN_HP)
    civilian_buriedness = read_with_exist_flag(bit_array, cls.SIZE_CIVILIAN_BURIEDNESS)
    civilian_damage = read_with_exist_flag(bit_array, cls.SIZE_CIVILIAN_DAMAGE)
    raw_civilian_position = read_with_exist_flag(bit_array, cls.SIZE_CIVILIAN_POSITION)
    civilian_position = (
      EntityID(raw_civilian_position) if raw_civilian_position else None
    )
    civilian = Civilian(civilian_id or -1)
    civilian.set_hp(civilian_hp)
    civilian.set_buriedness(civilian_buriedness)
    civilian.set_damage(civilian_damage)
    civilian.set_position(civilian_position)
    return MessageCivilian(
      False,
      civilian,
      StandardMessagePriority.NORMAL,
      sender_entity_id,
      std_message.get_ttl(),
    )

  def __hash__(self) -> int:
    h = super().__hash__()
    return hash(
      (
        h,
        self._civilian_entity_id,
        self._civilian_hp,
        self._civilian_buriedness,
        self._civilian_damage,
        self._civilian_position,
      )
    )

  def __str__(self) -> str:
    return f"MessageCivilian(civilian_entity_id={self._civilian_entity_id}, civilian_hp={self._civilian_hp}, civilian_buriedness={self._civilian_buriedness}, civilian_damage={self._civilian_damage}, civilian_position={self._civilian_position})"
