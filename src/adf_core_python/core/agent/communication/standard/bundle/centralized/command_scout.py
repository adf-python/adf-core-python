from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from rcrscore.entities import EntityID

from adf_core_python.core.agent.communication.standard.bundle.standard_message import (
  StandardMessage,
)
from adf_core_python.core.agent.communication.standard.utility.bitarray_with_exits_flag import (
  read_with_exist_flag,
  write_with_exist_flag,
)

if TYPE_CHECKING:
  from adf_core_python.core.agent.communication.standard.bundle.standard_message_priority import (
    StandardMessagePriority,
  )
  from bitarray import bitarray


class CommandScout(StandardMessage):
  SIZE_AGENT_ENTITY_ID: int = 32
  SIZE_TARGET_ENTITY_ID: int = 32
  SIZE_SCOUT_RANGE: int = 32

  def __init__(
    self,
    is_wireless_message: bool,
    command_executor_agent_entity_id: EntityID,
    sender_entity_id: EntityID,
    scout_range: int,
    priority: StandardMessagePriority,
    command_target_entity_id: Optional[EntityID] = None,
  ):
    super().__init__(is_wireless_message, priority, sender_entity_id)
    self._command_executor_agent_entity_id: Optional[EntityID] = (
      command_executor_agent_entity_id
    )
    self._command_target_entity_id: Optional[EntityID] = command_target_entity_id
    self._is_bloadcast: bool = command_target_entity_id is None
    self._scout_range: Optional[int] = scout_range

  def get_command_executor_agent_entity_id(self) -> Optional[EntityID]:
    return self._command_executor_agent_entity_id

  def get_command_target_entity_id(self) -> Optional[EntityID]:
    return self._command_target_entity_id

  def get_scout_range(self) -> Optional[int]:
    return self._scout_range

  def is_broadcast(self) -> bool:
    return self._is_bloadcast

  def get_bit_size(self) -> int:
    return self.to_bits().__len__()

  def to_bits(self) -> bitarray:
    bit_array = super().to_bits()
    raw_command_executor_agent_entity_id = (
      self._command_executor_agent_entity_id.get_value()
      if self._command_executor_agent_entity_id is not None
      else None
    )
    write_with_exist_flag(
      bit_array,
      raw_command_executor_agent_entity_id,
      self.SIZE_AGENT_ENTITY_ID,
    )
    raw_command_target_entity_id = (
      self._command_target_entity_id.get_value()
      if self._command_target_entity_id is not None
      else None
    )
    write_with_exist_flag(
      bit_array, raw_command_target_entity_id, self.SIZE_TARGET_ENTITY_ID
    )
    write_with_exist_flag(bit_array, self._scout_range, self.SIZE_SCOUT_RANGE)

    return bit_array

  @classmethod
  def from_bits(
    cls,
    bit_array: bitarray,
    is_wireless_message: bool,
    sender_entity_id: EntityID,
  ) -> CommandScout:
    std_message = super().from_bits(bit_array, is_wireless_message, sender_entity_id)
    raw_command_executor_agent_entity_id = read_with_exist_flag(
      bit_array, cls.SIZE_AGENT_ENTITY_ID
    )
    command_executor_agent_id = (
      EntityID(raw_command_executor_agent_entity_id)
      if raw_command_executor_agent_entity_id is not None
      else None
    )
    raw_command_target_entity_id = read_with_exist_flag(
      bit_array, cls.SIZE_TARGET_ENTITY_ID
    )
    command_target_id = (
      EntityID(raw_command_target_entity_id)
      if raw_command_target_entity_id is not None
      else None
    )
    scout_range = read_with_exist_flag(bit_array, cls.SIZE_SCOUT_RANGE)
    return cls(
      is_wireless_message,
      command_executor_agent_id or EntityID(-1),
      sender_entity_id,
      scout_range if scout_range is not None else -1,
      std_message.get_priority(),
      command_target_id,
    )

  def __hash__(self) -> int:
    h = super().__hash__()
    return hash(
      (
        h,
        self._command_executor_agent_entity_id,
        self._command_target_entity_id,
        self._scout_range,
      )
    )

  def __str__(self) -> str:
    return f"CommandScout(executor={self._command_executor_agent_entity_id}, target={self._command_target_entity_id}, scout_range={self._scout_range})"
