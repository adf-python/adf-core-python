package adf_core_python.gateway.message;

import adf_core_python.gateway.message.urn.ModuleMessageComponentURN;
import adf_core_python.gateway.message.urn.ModuleMessageURN;
import rescuecore2.config.Config;
import rescuecore2.messages.AbstractMessage;
import rescuecore2.messages.components.ConfigComponent;
import rescuecore2.messages.components.EntityIDComponent;
import rescuecore2.messages.components.EntityListComponent;
import rescuecore2.messages.components.IntComponent;
import rescuecore2.messages.protobuf.RCRSProto;
import rescuecore2.worldmodel.Entity;
import rescuecore2.worldmodel.EntityID;

import java.io.IOException;
import java.io.InputStream;
import java.util.Collection;
import java.util.List;

public class AMAgent extends AbstractMessage {
    private final EntityIDComponent agentID;
    private final EntityListComponent entities;
    private final ConfigComponent config;
    private final IntComponent mode;

    public AMAgent(EntityID agentID, Collection<Entity> entities, Config config, int mode) {
        this();
        this.agentID.setValue(agentID);
        this.entities.setEntities(entities);
        this.config.setConfig(config);
        this.mode.setValue(mode);
    }

    public AMAgent(InputStream inputStream) throws IOException {
        this();
        read(inputStream);
    }

    public AMAgent(RCRSProto.MessageProto messageProto) {
        this();
        fromMessageProto(messageProto);
    }

    private AMAgent() {
        super(ModuleMessageURN.AM_AGENT);
        this.agentID = new EntityIDComponent(ModuleMessageComponentURN.AgentID);
        this.entities = new EntityListComponent(ModuleMessageComponentURN.Entities);
        this.config = new ConfigComponent(ModuleMessageComponentURN.Config);
        this.mode = new IntComponent(ModuleMessageComponentURN.Mode);
        addMessageComponent(agentID);
        addMessageComponent(entities);
        addMessageComponent(config);
        addMessageComponent(mode);
    }

    public EntityID getAgentID() {
        return this.agentID.getValue();
    }

    public List<Entity> getEntities() {
        return this.entities.getEntities();
    }

    public Config getConfig() {
        return this.config.getConfig();
    }

    public int getMode() {
        return this.mode.getValue();
    }
}
