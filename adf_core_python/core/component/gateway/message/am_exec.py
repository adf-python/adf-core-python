from abc import ABC
from typing import Any

from rcrs_core.connection import RCRSProto_pb2
from rcrs_core.messages.message import Message

from adf_core_python.core.component.gateway.message.urn.urn import (
    ModuleMSG,
    ComponentModuleMSG,
)


class AMExec(Message, ABC):
    def __init__(self) -> None:
        super().__init__(ModuleMSG.AM_EXEC)

    def read(self) -> None:
        pass

    def write(self, module_id: str, method_name: str) -> Any:
        msg = RCRSProto_pb2.MessageProto()
        msg.urn = self.get_urn()
        msg.components[ComponentModuleMSG.ModuleID].stringValue = module_id
        msg.components[ComponentModuleMSG.MethodName].stringValue = method_name

        return msg
