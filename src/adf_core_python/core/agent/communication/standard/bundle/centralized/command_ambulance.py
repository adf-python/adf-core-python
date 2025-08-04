from __future__ import annotations

from typing import Optional

from bitarray import bitarray
from rcrscore.entities import EntityID

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


class CommandAmbulance(StandardMessage):
    ACTION_REST: int = 0
    ACTION_MOVE: int = 1
    ACTION_RESCUE: int = 2
    ACTION_LOAD: int = 3
    ACTION_UNLOAD: int = 4
    ACTION_AUTONOMY: int = 5

    SIZE_AMBULANCE_TEAM_ENTITY_ID: int = 32
    SIZE_TARGET_ENTITY_ID: int = 32
    SIZE_ACTION: int = 4

    def __init__(
        self,
        is_wireless_message: bool,
        command_executor_agent_entity_id: EntityID,
        sender_entity_id: EntityID,
        execute_action: int,
        priority: StandardMessagePriority,
        command_target_entity_id: Optional[EntityID] = None,
    ):
        super().__init__(is_wireless_message, priority, sender_entity_id)
        self._command_executor_agent_entity_id: Optional[EntityID] = (
            command_executor_agent_entity_id
        )
        self._command_target_entity_id: Optional[EntityID] = command_target_entity_id
        self._is_bloadcast: bool = command_target_entity_id is None
        self._execute_action: Optional[int] = execute_action

    def get_command_executor_agent_entity_id(self) -> Optional[EntityID]:
        return self._command_executor_agent_entity_id

    def get_command_target_entity_id(self) -> Optional[EntityID]:
        return self._command_target_entity_id

    def get_execute_action(self) -> Optional[int]:
        return self._execute_action

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
            self.SIZE_AMBULANCE_TEAM_ENTITY_ID,
        )
        raw_command_target_entity_id = (
            self._command_target_entity_id.get_value()
            if self._command_target_entity_id is not None
            else None
        )
        write_with_exist_flag(
            bit_array, raw_command_target_entity_id, self.SIZE_TARGET_ENTITY_ID
        )
        write_with_exist_flag(bit_array, self._execute_action, self.SIZE_ACTION)
        return bit_array

    @classmethod
    def from_bits(
        cls,
        bit_array: bitarray,
        is_wireless_message: bool,
        sender_entity_id: EntityID,
    ) -> CommandAmbulance:
        std_message = super().from_bits(
            bit_array, is_wireless_message, sender_entity_id
        )
        raw_command_executor_agent_entity_id = read_with_exist_flag(
            bit_array, cls.SIZE_AMBULANCE_TEAM_ENTITY_ID
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
        execute_action = read_with_exist_flag(bit_array, cls.SIZE_ACTION)
        return cls(
            is_wireless_message,
            command_executor_agent_id or EntityID(-1),
            sender_entity_id,
            execute_action if execute_action is not None else -1,
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
                self._execute_action,
            )
        )

    def __str__(self) -> str:
        return f"CommandAmbulance(executor={self._command_executor_agent_entity_id}, target={self._command_target_entity_id}, action={self._execute_action})"
