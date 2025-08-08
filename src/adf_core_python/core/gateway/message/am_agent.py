from typing import Any

from rcrscore.entities import EntityID
from rcrscore.entities.entity import Entity
from rcrscore.messages import AKControlMessage
from rcrscore.proto import RCRSProto_pb2
from rcrscore.urn.control_message import ControlMessageURN

from adf_core_python.core.gateway.message.urn.urn import (
  ComponentModuleMSG,
  ModuleMSG,
)


class AMAgent(AKControlMessage):
  @staticmethod
  def write(
    agent_id: EntityID,
    entities: list[Entity],
    config: dict[str, Any],
    mode: int,
  ) -> RCRSProto_pb2.MessageProto:
    entity_proto_list = []
    for entity in entities:
      entity_proto = RCRSProto_pb2.EntityProto()
      entity_proto.urn = entity.get_urn()
      entity_proto.entityID = entity.get_entity_id().get_value()

      property_proto_list = []
      for k, v in entity.get_properties().items():
        property_proto_list.append(v.to_property_proto())
      entity_proto.properties.extend(property_proto_list)
      entity_proto_list.append(entity_proto)

    entity_list_proto = RCRSProto_pb2.EntityListProto()
    entity_list_proto.entities.extend(entity_proto_list)

    config_proto = RCRSProto_pb2.ConfigProto()
    for key, value in config.items():
      config_proto.data[str(key)] = str(value)

    msg = RCRSProto_pb2.MessageProto()
    msg.urn = AMAgent.get_urn()
    msg.components[ComponentModuleMSG.AgentID].entityID = agent_id.get_value()
    msg.components[ComponentModuleMSG.Entities].entityList.CopyFrom(entity_list_proto)
    msg.components[ComponentModuleMSG.Config].config.CopyFrom(config_proto)
    msg.components[ComponentModuleMSG.Mode].intValue = mode
    return msg

  @staticmethod
  def get_urn() -> ControlMessageURN:
    return ModuleMSG.AM_AGENT  # type: ignore
