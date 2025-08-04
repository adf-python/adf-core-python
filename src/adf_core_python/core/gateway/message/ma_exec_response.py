from rcrscore.config.config import Config
from rcrscore.messages import KAControlMessage
from rcrscore.proto import RCRSProto_pb2
from rcrscore.urn.control_message import ControlMessageURN

from adf_core_python.core.gateway.message.urn.urn import (
    ComponentModuleMSG,
    ModuleMSG,
)


class MAExecResponse(KAControlMessage):
    def __init__(self, message_proto: RCRSProto_pb2.MessageProto) -> None:
        self.result = Config()
        self.read(message_proto)

    def read(self, message_proto: RCRSProto_pb2.MessageProto) -> None:
        self.module_id: str = message_proto.components[
            ComponentModuleMSG.ModuleID
        ].stringValue
        result = message_proto.components[ComponentModuleMSG.Result].config
        for key, value in result.data.items():
            self.result.set_value(key, value)

    @staticmethod
    def get_urn() -> ControlMessageURN:
        return ModuleMSG.MA_EXEC_RESPONSE  # type: ignore
