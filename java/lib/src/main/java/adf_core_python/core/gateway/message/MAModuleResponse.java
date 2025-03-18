package adf_core_python.core.gateway.message;

import adf_core_python.core.gateway.message.urn.ModuleMessageComponentURN;
import adf_core_python.core.gateway.message.urn.ModuleMessageURN;
import rescuecore2.messages.AbstractMessage;
import rescuecore2.messages.components.StringComponent;
import rescuecore2.messages.protobuf.RCRSProto;

import java.io.IOException;
import java.io.InputStream;

public class MAModuleResponse extends AbstractMessage {
    private final StringComponent moduleID;
    private final StringComponent className;

    public MAModuleResponse(String moduleID, String className) {
        this();
        this.moduleID.setValue(moduleID);
        this.className.setValue(className);
    }

    public MAModuleResponse(InputStream inputStream) throws IOException {
        this();
        read(inputStream);
    }

    public MAModuleResponse(RCRSProto.MessageProto messageProto) {
        this();
        fromMessageProto(messageProto);
    }

    private MAModuleResponse() {
        super(ModuleMessageURN.MA_MODULE_RESPONSE);
        this.moduleID = new StringComponent(ModuleMessageComponentURN.ModuleID);
        this.className = new StringComponent(ModuleMessageComponentURN.ClassName);
        addMessageComponent(moduleID);
        addMessageComponent(className);
    }

    public String getModuleID() {
        return this.moduleID.getValue();
    }

    public String getClassName() {
        return this.className.getValue();
    }
}
