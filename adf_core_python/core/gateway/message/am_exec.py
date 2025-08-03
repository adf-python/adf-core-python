from typing import Any

from rcrscore.messages import AKControlMessage
from rcrscore.proto import RCRSProto_pb2
from rcrscore.urn.control_message import ControlMessageURN

from adf_core_python.core.gateway.message.urn.urn import (
    ComponentModuleMSG,
    ModuleMSG,
)


class AMExec(AKControlMessage):
    @staticmethod
    def write(module_id: str, method_name: str, arguments: dict[str, str]) -> Any:
        msg = RCRSProto_pb2.MessageProto()
        msg.urn = AMExec.get_urn()
        msg.components[ComponentModuleMSG.ModuleID].stringValue = module_id
        msg.components[ComponentModuleMSG.MethodName].stringValue = method_name
        config_proto = RCRSProto_pb2.ConfigProto()
        for key, value in arguments.items():
            config_proto.data[key] = value
        msg.components[ComponentModuleMSG.Arguments].config.CopyFrom(config_proto)

        return msg

    @staticmethod
    def get_urn() -> ControlMessageURN:
        return ModuleMSG.AM_EXEC  # type: ignore
