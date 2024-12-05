from enum import IntEnum


class ModuleMSG(IntEnum):
    AM_AGENT = 0x0301
    AM_MODULE = 0x0302
    MA_MODULE_RESPONSE = 0x0303
    AM_UPDATE = 0x0304
    AM_EXEC = 0x0305


class ComponentModuleMSG(IntEnum):
    AgentID = 0x0401
    Entities = 0x0402
    ModuleName = 0x0403
    DefaultClassName = 0x0404
    ModuleID = 0x0405
    ClassNames = 0x0406
    Time = 0x0407
    Changed = 0x0408
    Heard = 0x0409
    MethodName = 0x0410
