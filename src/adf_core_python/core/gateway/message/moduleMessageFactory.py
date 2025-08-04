from typing import Optional

from rcrscore.proto import RCRSProto_pb2

from adf_core_python.core.gateway.message.ma_exec_response import MAExecResponse
from adf_core_python.core.gateway.message.ma_module_response import (
    MAModuleResponse,
)
from adf_core_python.core.gateway.message.urn.urn import ModuleMSG


class ModuleMessageFactory:
    def __init__(self) -> None:
        pass

    def make_message(
        self, msg: RCRSProto_pb2.MessageProto
    ) -> Optional[MAModuleResponse | MAExecResponse]:
        if msg.urn == ModuleMSG.MA_MODULE_RESPONSE:
            return MAModuleResponse(msg)
        elif msg.urn == ModuleMSG.MA_EXEC_RESPONSE:
            return MAExecResponse(msg)

        return None
