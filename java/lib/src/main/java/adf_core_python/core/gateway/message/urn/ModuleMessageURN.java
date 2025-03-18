package adf_core_python.core.gateway.message.urn;

import rescuecore2.URN;

import java.util.Map;

public enum ModuleMessageURN implements URN {
    AM_AGENT(0x0300 | 1, "urn:adf_core_python.gateway.messages:am_agent"),
    AM_MODULE(0x0300 | 2, "urn:adf_core_python.gateway.messages:am_module"),
    MA_MODULE_RESPONSE(0x0300 | 3, "urn:adf_core_python.gateway.messages:am_module_response"),
    AM_UPDATE(0x0300 | 4, "urn:adf_core_python.gateway.messages:am_update"),
    AM_EXEC(0x0300 | 5, "urn:adf_core_python.gateway.messages:am_exec"),
    MA_EXEC_RESPONSE(0x0300 | 6, "urn:adf_core_python.gateway.messages:am_exec_response");

    public static final Map<Integer, ModuleMessageURN> MAP = URN.generateMap(ModuleMessageURN.class);
    public static final Map<String, ModuleMessageURN> MAP_STR = URN.generateMapStr(ModuleMessageURN.class);
    private final int urnId;
    private final String urnStr;

    private ModuleMessageURN(int urnId, String urnStr) {
        this.urnId = urnId;
        this.urnStr = urnStr;
    }

    public static ModuleMessageURN fromInt(int s) {
        return MAP.get(s);
    }

    public static ModuleMessageURN fromString(String urn) {
        return MAP_STR.get(urn);
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
