from abc import ABC
from typing import Any

from rcrs_core.commands.Command import Command
from rcrs_core.connection import RCRSProto_pb2
from rcrs_core.messages.message import Message
from rcrs_core.worldmodel.changeSet import ChangeSet

from adf_core_python.core.gateway.message.urn.urn import (
    ModuleMSG,
    ComponentModuleMSG,
)


class AMUpdate(Message, ABC):
    def __init__(self) -> None:
        super().__init__(ModuleMSG.AM_UPDATE)

    def read(self) -> None:
        pass

    def write(self, time: int, changed: ChangeSet, heard: list[Command]) -> Any:
        msg = RCRSProto_pb2.MessageProto()
        msg.urn = self.get_urn()
        msg.components[ComponentModuleMSG.Time].intValue = time
        msg.components[ComponentModuleMSG.Changed].changeSet.CopyFrom(
            changed.to_change_set_proto()
        )
        message_list_proto = RCRSProto_pb2.MessageListProto()
        message_proto_list = []
        if heard is not None:
            for h in heard:
                message_proto_list.append(h.prepare_cmd())
        message_list_proto.commands.extend(message_proto_list)
        msg.components[ComponentModuleMSG.Heard].commandList.CopyFrom(
            message_list_proto
        )
        return msg
