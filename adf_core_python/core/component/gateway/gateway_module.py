import uuid

from adf_core_python.core.component.gateway.gateway_agent import GatewayAgent
from adf_core_python.core.component.gateway.message.am_exec import AMExec
from adf_core_python.core.component.gateway.message.am_module import AMModule


class GatewayModule:
    def __init__(self, gateway_agent: GatewayAgent):
        self._gateway_agent = gateway_agent
        self._module_id: str = str(uuid.uuid4())
        self._class_names: [str] = []

    def get_module_id(self) -> str:
        return self._module_id

    def get_class_names(self) -> [str]:
        return self._class_names

    def set_class_names(self, class_names: [str]):
        self._class_names = class_names

    def initialize(self, module_name: str, default_class_name: str):
        if not self._gateway_agent.is_initialized():
            self._gateway_agent.initialize()
        am_module = AMModule()
        self._gateway_agent.send_msg(
            am_module.write(
                self._gateway_agent.get_agent_entity_id(),
                self._module_id,
                module_name,
                default_class_name,
            )
        )

    def execute(self, method_name: str, *args):
        am_exec = AMExec()
        self._gateway_agent.send_msg(am_exec.write(self._module_id, method_name))
