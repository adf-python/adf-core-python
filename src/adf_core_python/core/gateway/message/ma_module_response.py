from abc import ABC
from typing import Optional

from rcrscore.messages import KAControlMessage
from rcrscore.proto import RCRSProto_pb2
from rcrscore.urn.control_message import ControlMessageURN

from adf_core_python.core.gateway.message.urn.urn import (
  ComponentModuleMSG,
  ModuleMSG,
)


class MAModuleResponse(KAControlMessage, ABC):
  def __init__(self, message_proto: RCRSProto_pb2.MessageProto) -> None:
    self.module_id: Optional[str] = None
    self.class_name: Optional[str] = None
    self.read(message_proto)

  def read(self, message_proto: RCRSProto_pb2.MessageProto) -> None:
    self.module_id = message_proto.components[ComponentModuleMSG.ModuleID].stringValue
    self.class_name = message_proto.components[ComponentModuleMSG.ClassName].stringValue

  @staticmethod
  def get_urn() -> ControlMessageURN:
    return ModuleMSG.MA_MODULE_RESPONSE  # type: ignore
