package adf_core_python.gateway.message;

import adf_core_python.gateway.message.urn.ModuleMessageComponentURN;
import adf_core_python.gateway.message.urn.ModuleMessageURN;
import rescuecore2.messages.AbstractMessage;
import rescuecore2.messages.components.StringComponent;
import rescuecore2.messages.protobuf.RCRSProto;

import java.io.IOException;
import java.io.InputStream;

public class AMModule extends AbstractMessage {
    private final StringComponent moduleID;
    private final StringComponent moduleName;
    private final StringComponent defaultClassName;

    public AMModule(String moduleID, String moduleName, String defaultClassName) {
        this();
        this.moduleID.setValue(moduleID);
        this.moduleName.setValue(moduleName);
        this.defaultClassName.setValue(defaultClassName);
    }

    public AMModule(InputStream inputStream) throws IOException {
        this();
        read(inputStream);
    }

    public AMModule(RCRSProto.MessageProto messageProto) {
        this();
        fromMessageProto(messageProto);
    }

    private AMModule() {
        super(ModuleMessageURN.AM_MODULE);
        this.moduleID = new StringComponent(ModuleMessageComponentURN.ModuleID);
        this.moduleName = new StringComponent(ModuleMessageComponentURN.ModuleName);
        this.defaultClassName = new StringComponent(ModuleMessageComponentURN.DefaultClassName);
        addMessageComponent(moduleID);
        addMessageComponent(moduleName);
        addMessageComponent(defaultClassName);
    }

    public String getModuleID() {
        return this.moduleID.getValue();
    }

    public String getModuleName() {
        return this.moduleName.getValue();
    }

    public String getDefaultClassName() {
        return this.defaultClassName.getValue();
    }
}
