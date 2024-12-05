from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.info.agent_info import AgentInfo
from adf_core_python.core.agent.info.world_info import WorldInfo
from adf_core_python.core.component.gateway.message.am_agent import AMAgent
from adf_core_python.core.component.gateway.message.am_update import AMUpdate
from adf_core_python.core.component.gateway.message.ma_module_response import (
    MAModuleResponse,
)
from adf_core_python.core.component.gateway.message.moduleMessageFactory import (
    ModuleMessageFactory,
)
from adf_core_python.core.logger.logger import get_logger

if TYPE_CHECKING:
    from adf_core_python.core.component.gateway.gateway_launcher import GatewayLauncher
    from adf_core_python.core.component.gateway.gateway_module import GatewayModule


class GatewayAgent:
    def __init__(self, gateway_launcher: GatewayLauncher) -> None:
        self._gateway_launcher = gateway_launcher
        self.send_msg = None
        self._is_initialized = False
        self._agent_info: Optional[AgentInfo] = None
        self._world_info: Optional[WorldInfo] = None
        self._time = None
        self._change_set = None
        self._hear = None
        self._gateway_modules: dict[str, GatewayModule] = {}
        self._logger = get_logger("GatewayAgent")

    def get_agent_entity_id(self) -> EntityID:
        return self._agent_info.get_entity_id()

    def get_module_count(self) -> int:
        return len(self._gateway_modules)

    def add_gateway_module(self, gateway_module: GatewayModule) -> None:
        self._gateway_modules[gateway_module.get_module_id()] = gateway_module

    def is_initialized(self) -> bool:
        return self._is_initialized

    def set_initialize_data(self, agent_info: AgentInfo, world_info: WorldInfo) -> None:
        self._agent_info = agent_info
        self._world_info = world_info

    def initialize(self) -> None:
        self._logger.info(
            type(list(self._world_info.get_world_model().get_entities())[0])
        )
        am_agent = AMAgent()
        self.send_msg(
            am_agent.write(
                self._agent_info.get_entity_id(),
                list(self._world_info.get_world_model().get_entities()),
            )
        )
        self._logger.info(
            "Sent AMAgent ( EntityID: " + str(self._agent_info.get_entity_id())
        )
        self._is_initialized = True

    def set_update_data(self, time, change_set, hear):
        self._time = time
        self._change_set = change_set
        self._hear = hear
        pass

    def update(self):
        am_update = AMUpdate()
        self.send_msg(
            am_update.write(
                self._agent_info.get_entity_id(),
                self._agent_info.get_time(),
                self._world_info.get_change_set(),
                None,
            )
        )

    def set_send_msg(self, connection_send_func):
        self.send_msg = connection_send_func

    def message_received(self, msg):
        c_msg = ModuleMessageFactory().make_message(msg)
        if isinstance(c_msg, MAModuleResponse):
            self._gateway_modules[msg.module_id].set_class_names(msg.class_names)
