package adf_core_python.core.gateway.message;

import adf_core_python.core.gateway.message.urn.ModuleMessageComponentURN;
import adf_core_python.core.gateway.message.urn.ModuleMessageURN;
import rescuecore2.config.Config;
import rescuecore2.messages.AbstractMessage;
import rescuecore2.messages.components.ConfigComponent;
import rescuecore2.messages.components.StringComponent;
import rescuecore2.messages.protobuf.RCRSProto;

import java.io.IOException;
import java.io.InputStream;

public class MAExecResponse extends AbstractMessage {
    private final StringComponent moduleID;
    private final ConfigComponent result;

    public MAExecResponse(String moduleID, Config result) {
        this();
        this.moduleID.setValue(moduleID);
        this.result.setConfig(result);
    }

    public MAExecResponse(InputStream inputStream) throws IOException {
        this();
        read(inputStream);
    }

    public MAExecResponse(RCRSProto.MessageProto messageProto) {
        this();
        fromMessageProto(messageProto);
    }

    private MAExecResponse() {
        super(ModuleMessageURN.MA_EXEC_RESPONSE);
        this.moduleID = new StringComponent(ModuleMessageComponentURN.ModuleID);
        this.result = new ConfigComponent(ModuleMessageComponentURN.Result);
        addMessageComponent(moduleID);
        addMessageComponent(result);
    }

    public String getModuleID() {
        return this.moduleID.getValue();
    }

    public Config getResult() {
        return this.result.getConfig();
    }
}
