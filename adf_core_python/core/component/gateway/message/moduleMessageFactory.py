from adf_core_python.core.component.gateway.message.am_agent import AMAgent
from adf_core_python.core.component.gateway.message.am_exec import AMExec
from adf_core_python.core.component.gateway.message.am_module import AMModule
from adf_core_python.core.component.gateway.message.am_update import AMUpdate
from adf_core_python.core.component.gateway.message.ma_module_response import (
    MAModuleResponse,
)
from adf_core_python.core.component.gateway.message.urn.urn import ModuleMSG


class ModuleMessageFactory:
    def __init__(self) -> None:
        pass

    def make_message(self, msg):
        if msg.urn == ModuleMSG.AM_AGENT:
            return AMAgent(msg)
        elif msg.urn == ModuleMSG.AM_MODULE:
            return AMModule(msg)
        elif msg.urn == ModuleMSG.MA_MODULE_RESPONSE:
            return MAModuleResponse(msg)
        elif msg.urn == ModuleMSG.AM_UPDATE:
            return AMUpdate(msg)
        elif msg.urn == ModuleMSG.AM_EXEC:
            return AMExec(msg)

        return None
