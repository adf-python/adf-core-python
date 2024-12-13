package adf_core_python.gateway.message;

import adf_core_python.gateway.message.urn.ModuleMessageComponentURN;
import adf_core_python.gateway.message.urn.ModuleMessageURN;
import rescuecore2.config.Config;
import rescuecore2.messages.AbstractMessage;
import rescuecore2.messages.components.ConfigComponent;
import rescuecore2.messages.components.StringComponent;
import rescuecore2.messages.protobuf.RCRSProto;

import java.io.IOException;
import java.io.InputStream;

public class AMExec extends AbstractMessage {
    private final StringComponent moduleID;
    private final StringComponent methodName;
    private final ConfigComponent arguments;

    public AMExec(String moduleID, String methodName, Config arguments) {
        this();
        this.moduleID.setValue(moduleID);
        this.methodName.setValue(methodName);
        this.arguments.setConfig(arguments);
    }

    public AMExec(InputStream inputStream) throws IOException {
        this();
        read(inputStream);
    }

    public AMExec(RCRSProto.MessageProto messageProto) {
        this();
        fromMessageProto(messageProto);
    }

    private AMExec() {
        super(ModuleMessageURN.AM_MODULE);
        this.moduleID = new StringComponent(ModuleMessageComponentURN.ModuleID);
        this.methodName = new StringComponent(ModuleMessageComponentURN.MethodName);
        this.arguments = new ConfigComponent(ModuleMessageComponentURN.Arguments);
        addMessageComponent(moduleID);
        addMessageComponent(methodName);
        addMessageComponent(arguments);
    }

    public String getModuleID() {
        return this.moduleID.getValue();
    }

    public String getMethodName() {
        return this.methodName.getValue();
    }

    public Config getArguments() {
        return this.arguments.getConfig();
    }
}
