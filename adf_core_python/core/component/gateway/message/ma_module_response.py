from abc import ABC

from rcrs_core.connection import RCRSProto_pb2
from rcrs_core.messages.message import Message

from adf_core_python.core.component.gateway.message.urn.urn import (
    ModuleMSG,
    ComponentModuleMSG,
)


class MAModuleResponse(Message, ABC):
    def __init__(self, data: RCRSProto_pb2) -> None:
        super().__init__(ModuleMSG)
        self.module_id = None
        self.class_names = None
        self.data = data

    def read(self) -> None:
        self.module_id = self.data.components[ComponentModuleMSG.ModuleID].stringValue
        self.class_names = self.data.components[
            ComponentModuleMSG.ClassNames
        ].stringList

    def write(self) -> None:
        pass
