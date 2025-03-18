package adf_core_python.core.gateway.message;

import adf_core_python.core.gateway.message.urn.ModuleMessageURN;
import rescuecore2.messages.Message;
import rescuecore2.messages.protobuf.RCRSProto.MessageProto;

import java.io.IOException;
import java.io.InputStream;

public class ModuleControlMessageFactory {
    public static Message makeMessage(int urn, InputStream inputStream) throws IOException {
        return makeMessage(ModuleMessageURN.fromInt(urn), inputStream);
    }

    public static Message makeMessage(ModuleMessageURN urn, InputStream inputStream) throws IOException {
        switch (urn) {
            case AM_AGENT -> new AMAgent(inputStream);
            case AM_MODULE -> new AMModule(inputStream);
            case MA_MODULE_RESPONSE -> new MAModuleResponse(inputStream);
            case AM_UPDATE -> new AMUpdate(inputStream);
            case AM_EXEC -> new AMExec(inputStream);
        }
        return null;
    }

    public static Message makeMessage(int urn, MessageProto messageProto) throws IOException {
        return makeMessage(ModuleMessageURN.fromInt(urn), messageProto);
    }

    public static Message makeMessage(ModuleMessageURN urn, MessageProto messageProto) {
        if (urn.equals(ModuleMessageURN.AM_AGENT)) {
            return new AMAgent(messageProto);
        } else if (urn.equals(ModuleMessageURN.AM_MODULE)) {
            return new AMModule(messageProto);
        } else if (urn.equals(ModuleMessageURN.AM_UPDATE)) {
            return new AMUpdate(messageProto);
        } else if (urn.equals(ModuleMessageURN.AM_EXEC)) {
            return new AMExec(messageProto);
        }
        return null;
    }
}
