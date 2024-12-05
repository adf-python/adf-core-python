from abc import ABC
from typing import Any

from rcrs_core.connection import RCRSProto_pb2
from rcrs_core.messages.message import Message
from rcrs_core.worldmodel.changeSet import ChangeSet
from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.component.gateway.message.urn.urn import (
    ModuleMSG,
    ComponentModuleMSG,
)


class AMUpdate(Message, ABC):
    def __init__(self) -> None:
        super().__init__(ModuleMSG.AM_UPDATE)

    def read(self) -> None:
        pass

    def write(self, agent_id: EntityID, time: int, changed: ChangeSet, heard) -> Any:
        msg = RCRSProto_pb2.MessageProto()
        msg.urn = self.get_urn()
        msg.components[ComponentModuleMSG.AgentID].entityID = agent_id.get_value()
        msg.components[ComponentModuleMSG.Time].intValue = time
        msg.components[ComponentModuleMSG.Changed].changeSet = changed
        msg.components[ComponentModuleMSG.Heard].commandList = heard

        return msg
