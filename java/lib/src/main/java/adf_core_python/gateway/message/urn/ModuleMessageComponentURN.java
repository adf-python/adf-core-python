package adf_core_python.gateway.message.urn;

import rescuecore2.URN;

import java.util.Map;

public enum ModuleMessageComponentURN implements URN {
    AgentID(0x0400 | 1, "Agent ID"),
    Entities(0x0400 | 2, "Entities"),
    Config(0x0400 | 3, "Entities"),
    Mode(0x0400 | 4, "Entities"),
    ModuleID(0x0400 | 5, "Module ID"),
    ModuleName(0x0400 | 6, "Module Name"),
    DefaultClassName(0x0400 | 7, "Default Class Name"),
    ClassName(0x0400 | 8, "Class Name"),
    Time(0x0400 | 9, "Time"),
    Changed(0x0400 | 10, "Changed"),
    Heard(0x0400 | 11, "Heard"),
    MethodName(0x0400 | 12, "Method Name"),
    Arguments(0x0400 | 13, "Arguments"),
    Result(0x0400 | 14, "Result");


    public static final Map<Integer, ModuleMessageComponentURN> MAP = URN.generateMap(ModuleMessageComponentURN.class);
    public static final Map<String, ModuleMessageComponentURN> MAP_STR = URN
            .generateMapStr(ModuleMessageComponentURN.class);
    private final int urnId;
    private final String urnStr;

    ModuleMessageComponentURN(int urnId, String urnStr) {
        this.urnId = urnId;
        this.urnStr = urnStr;
    }

    public static ModuleMessageComponentURN fromInt(int urnId) {
        return MAP.get(urnId);
    }

    public static ModuleMessageComponentURN fromString(String urnStr) {
        return MAP_STR.get(urnStr);
    }

    @Override
    public int getURNId() {
        return urnId;
    }

    @Override
    public String getURNStr() {
        return urnStr;
    }
}
