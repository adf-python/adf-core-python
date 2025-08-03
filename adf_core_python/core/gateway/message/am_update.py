from typing import Any

from rcrscore.commands import Command
from rcrscore.messages import AKControlMessage
from rcrscore.proto import RCRSProto_pb2
from rcrscore.urn.control_message import ControlMessageURN
from rcrscore.worldmodel import ChangeSet

from adf_core_python.core.gateway.message.urn.urn import (
    ComponentModuleMSG,
    ModuleMSG,
)


class AMUpdate(AKControlMessage):
    @staticmethod
    def write(time: int, changed: ChangeSet, heard: list[Command]) -> Any:
        msg = RCRSProto_pb2.MessageProto()
        msg.urn = AMUpdate.get_urn()
        msg.components[ComponentModuleMSG.Time].intValue = time
        msg.components[ComponentModuleMSG.Changed].changeSet.CopyFrom(
            changed.to_change_set_proto()
        )
        message_list_proto = RCRSProto_pb2.MessageListProto()
        message_proto_list = []
        if heard is not None:
            for h in heard:
                message_proto_list.append(h.to_message_proto())
        message_list_proto.commands.extend(message_proto_list)
        msg.components[ComponentModuleMSG.Heard].commandList.CopyFrom(
            message_list_proto
        )
        return msg

    @staticmethod
    def get_urn() -> ControlMessageURN:
        return ModuleMSG.AM_UPDATE  # type: ignore
