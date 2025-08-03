import uuid
from typing import Optional

from rcrscore.config.config import Config

from adf_core_python.core.gateway.gateway_agent import GatewayAgent
from adf_core_python.core.gateway.message.am_exec import AMExec
from adf_core_python.core.gateway.message.am_module import AMModule


class GatewayModule:
    def __init__(self, gateway_agent: GatewayAgent):
        self._gateway_agent = gateway_agent
        self._module_id: str = str(uuid.uuid4())
        self._is_initialized = False
        self._is_executed = False
        self._gateway_class_name: str = ""
        self._result: Optional[Config] = None
        self._gateway_agent.add_gateway_module(self)

    def get_module_id(self) -> str:
        return self._module_id

    def get_gateway_class_name(self) -> str:
        return self._gateway_class_name

    def set_gateway_class_name(self, gateway_class_name: str) -> None:
        self._gateway_class_name = gateway_class_name

    def get_is_initialized(self) -> bool:
        return self._is_initialized

    def set_is_initialized(self, is_initialized: bool) -> None:
        self._is_initialized = is_initialized

    def initialize(self, module_name: str, default_class_name: str) -> str:
        if not self._gateway_agent.is_initialized():
            self._gateway_agent.initialize()
        if self._gateway_agent.send_msg is None:
            raise RuntimeError("send_msg is None")

        am_module = AMModule()
        self._gateway_agent.send_msg(
            am_module.write(
                self._module_id,
                module_name,
                default_class_name,
            )
        )

        while not self.get_is_initialized():
            pass

        return self.get_gateway_class_name()

    def get_execute_response(self) -> Config:
        if self._result is None:
            raise RuntimeError("No execution result available")
        return self._result

    def set_execute_response(self, result: Config) -> None:
        self._result = result

    def get_is_executed(self) -> bool:
        return self._is_executed

    def set_is_executed(self, _is_executed: bool) -> None:
        self._is_executed = _is_executed

    def execute(
        self, method_name: str, args: Optional[dict[str, str]] = None
    ) -> Config:
        if args is None:
            args = {}
        if self._gateway_agent.send_msg is None:
            raise RuntimeError("send_msg is None")

        am_exec = AMExec()
        self._gateway_agent.send_msg(am_exec.write(self._module_id, method_name, args))

        while not self.get_is_executed():
            pass

        self.set_is_executed(False)
        return self.get_execute_response()
