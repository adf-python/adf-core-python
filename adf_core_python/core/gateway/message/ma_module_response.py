from abc import ABC
from typing import Optional

from rcrs_core.connection import RCRSProto_pb2
from rcrs_core.messages.message import Message

from adf_core_python.core.gateway.message.urn.urn import (
    ModuleMSG,
    ComponentModuleMSG,
)


class MAModuleResponse(Message, ABC):
    def __init__(self, data: RCRSProto_pb2) -> None:
        super().__init__(ModuleMSG.MA_MODULE_RESPONSE)
        self.module_id: Optional[str] = None
        self.class_name: Optional[str] = None
        self.data = data
        self.read()

    def read(self) -> None:
        self.module_id = self.data.components[ComponentModuleMSG.ModuleID].stringValue
        self.class_name = self.data.components[ComponentModuleMSG.ClassName].stringValue

    def write(self) -> None:
        pass
