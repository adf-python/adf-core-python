from typing import Any

from rcrs_core.connection import RCRSProto_pb2
from rcrs_core.entities.entity import Entity
from rcrs_core.messages.message import Message
from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.component.gateway.message.urn.urn import (
    ModuleMSG,
    ComponentModuleMSG,
)


class AMAgent(Message):
    def __init__(self) -> None:
        super().__init__(ModuleMSG.AM_AGENT)

    def read(self) -> None:
        pass

    def write(self, agent_id: EntityID, entities: list[Entity]) -> Any:
        entity_proto_list = []
        for entity in entities:
            entity_proto = RCRSProto_pb2.EntityProto()
            entity_proto.urn = entity.get_urn()
            entity_proto.entityID = entity.get_id()

            property_proto_list = []
            for k, v in entity.get_properties().items():
                property_proto_list.append(v.to_property_proto())
            entity_proto.properties.extend(property_proto_list)
            entity_proto_list.append(entity_proto)

        entity_list_proto = RCRSProto_pb2.EntityListProto()
        entity_list_proto.entities.extend(entity_proto_list)
        msg = RCRSProto_pb2.MessageProto()
        msg.urn = self.get_urn()
        msg.components[ComponentModuleMSG.AgentID].entityID = agent_id.get_value()
        msg.components[ComponentModuleMSG.Entities].entityList = entity_list_proto
        return msg
