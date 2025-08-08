from enum import IntEnum


class ModuleMSG(IntEnum):
  AM_AGENT = 0x0301
  AM_MODULE = 0x0302
  MA_MODULE_RESPONSE = 0x0303
  AM_UPDATE = 0x0304
  AM_EXEC = 0x0305
  MA_EXEC_RESPONSE = 0x0306


class ComponentModuleMSG(IntEnum):
  AgentID = 0x0401
  Entities = 0x0402
  Config = 0x0403
  Mode = 0x0404
  ModuleID = 0x0405
  ModuleName = 0x0406
  DefaultClassName = 0x0407
  ClassName = 0x0408
  Time = 0x0409
  Changed = 0x040A
  Heard = 0x040B
  MethodName = 0x040C
  Arguments = 0x040D
  Result = 0x040E
