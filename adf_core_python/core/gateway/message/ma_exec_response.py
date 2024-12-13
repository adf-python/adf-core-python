from abc import ABC

from rcrs_core.config.config import Config
from rcrs_core.connection import RCRSProto_pb2
from rcrs_core.messages.message import Message

from adf_core_python.core.gateway.message.urn.urn import (
    ModuleMSG,
    ComponentModuleMSG,
)


class MAExecResponse(Message, ABC):
    def __init__(self, data: RCRSProto_pb2) -> None:
        super().__init__(ModuleMSG.MA_EXEC_RESPONSE)
        self.module_id = None
        self.result = Config()
        self.data = data
        self.read()

    def read(self) -> None:
        self.module_id = self.data.components[ComponentModuleMSG.ModuleID].stringValue
        result = self.data.components[ComponentModuleMSG.Result].config
        for key, value in result.data.items():
            self.result.set_value(key, value)

    def write(self) -> None:
        pass
