from typing import Any

from rcrscore.messages import AKControlMessage
from rcrscore.proto import RCRSProto_pb2
from rcrscore.urn.control_message import ControlMessageURN

from adf_core_python.core.gateway.message.urn.urn import (
  ComponentModuleMSG,
  ModuleMSG,
)


class AMModule(AKControlMessage):
  @staticmethod
  def write(
    module_id: str,
    module_name: str,
    default_class_name: str,
  ) -> Any:
    msg = RCRSProto_pb2.MessageProto()
    msg.urn = AMModule.get_urn()
    msg.components[ComponentModuleMSG.ModuleID].stringValue = module_id
    msg.components[ComponentModuleMSG.ModuleName].stringValue = module_name
    msg.components[ComponentModuleMSG.DefaultClassName].stringValue = default_class_name

    return msg

  @staticmethod
  def get_urn() -> ControlMessageURN:
    return ModuleMSG.AM_MODULE  # type: ignore
