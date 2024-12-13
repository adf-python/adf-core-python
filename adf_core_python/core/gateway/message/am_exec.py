from abc import ABC
from typing import Any

from rcrs_core.connection import RCRSProto_pb2
from rcrs_core.messages.message import Message

from adf_core_python.core.gateway.message.urn.urn import (
    ModuleMSG,
    ComponentModuleMSG,
)


class AMExec(Message, ABC):
    def __init__(self) -> None:
        super().__init__(ModuleMSG.AM_EXEC)

    def read(self) -> None:
        pass

    def write(self, module_id: str, method_name: str, arguments: dict[str, str]) -> Any:
        msg = RCRSProto_pb2.MessageProto()
        msg.urn = self.get_urn()
        msg.components[ComponentModuleMSG.ModuleID].stringValue = module_id
        msg.components[ComponentModuleMSG.MethodName].stringValue = method_name
        config_proto = RCRSProto_pb2.ConfigProto()
        for key, value in arguments.items():
            config_proto.data[key] = value
        msg.components[ComponentModuleMSG.Arguments].config.CopyFrom(config_proto)

        return msg
