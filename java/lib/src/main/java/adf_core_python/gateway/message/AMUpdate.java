package adf_core_python.gateway.message;

import adf_core_python.gateway.message.urn.ModuleMessageComponentURN;
import adf_core_python.gateway.message.urn.ModuleMessageURN;
import rescuecore2.messages.AbstractMessage;
import rescuecore2.messages.Command;
import rescuecore2.messages.components.ChangeSetComponent;
import rescuecore2.messages.components.CommandListComponent;
import rescuecore2.messages.components.IntComponent;
import rescuecore2.messages.protobuf.RCRSProto;
import rescuecore2.worldmodel.ChangeSet;

import java.io.IOException;
import java.io.InputStream;
import java.util.Collection;
import java.util.List;

public class AMUpdate extends AbstractMessage {
    private final IntComponent time;
    private final ChangeSetComponent changed;
    private final CommandListComponent heard;

    public AMUpdate(int time, ChangeSet changed, Collection<Command> heard) {
        this();
        this.time.setValue(time);
        this.changed.setChangeSet(changed);
        this.heard.setCommands(heard);
    }

    public AMUpdate(InputStream inputStream) throws IOException {
        this();
        read(inputStream);
    }

    public AMUpdate(RCRSProto.MessageProto messageProto) {
        this();
        fromMessageProto(messageProto);
    }

    private AMUpdate() {
        super(ModuleMessageURN.AM_UPDATE);
        this.time = new IntComponent(ModuleMessageComponentURN.Time);
        this.changed = new ChangeSetComponent(ModuleMessageComponentURN.Changed);
        this.heard = new CommandListComponent(ModuleMessageComponentURN.Heard);
        addMessageComponent(this.time);
        addMessageComponent(this.changed);
        addMessageComponent(this.heard);
    }

    public int getTime() {
        return this.time.getValue();
    }

    public ChangeSet getChanged() {
        return this.changed.getChangeSet();
    }

    public List<Command> getHeard() {
        return this.heard.getCommands();
    }
}
