from typing import Any

from rcrs_core.connection import RCRSProto_pb2
from rcrs_core.messages.message import Message

from adf_core_python.core.gateway.message.urn.urn import (
    ModuleMSG,
    ComponentModuleMSG,
)


class AMModule(Message):
    def __init__(self) -> None:
        super().__init__(ModuleMSG.AM_MODULE)

    def read(self) -> None:
        pass

    def write(
        self,
        module_id: str,
        module_name: str,
        default_class_name: str,
    ) -> Any:
        msg = RCRSProto_pb2.MessageProto()
        msg.urn = self.get_urn()
        msg.components[ComponentModuleMSG.ModuleID].stringValue = module_id
        msg.components[ComponentModuleMSG.ModuleName].stringValue = module_name
        msg.components[
            ComponentModuleMSG.DefaultClassName
        ].stringValue = default_class_name

        return msg
