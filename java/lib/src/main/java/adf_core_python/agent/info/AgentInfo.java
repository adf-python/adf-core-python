package adf_core_python.agent.info;

import adf.core.agent.action.Action;
import jakarta.annotation.Nonnull;
import jakarta.annotation.Nullable;
import rescuecore2.messages.Command;
import rescuecore2.standard.entities.*;
import rescuecore2.worldmodel.ChangeSet;
import rescuecore2.worldmodel.EntityID;

import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

public class AgentInfo {
    private final EntityID entityID;
    private final StandardWorldModel worldModel;
    private int time;
    private ChangeSet changed;
    private Collection<Command> heard;
    private long thinkStartTime;

    private Map<Integer, Action> actionHistory;

    public AgentInfo(@Nonnull EntityID entityID, @Nonnull StandardWorldModel worldModel) {
        this.entityID = entityID;
        this.worldModel = worldModel;
        this.time = 0;
        this.actionHistory = new HashMap<>();
        recordThinkStartTime();
    }

    public int getTime() {
        return this.time;
    }

    public void setTime(int time) {
        this.time = time;
    }

    @Nullable
    public Collection<Command> getHeard() {
        return this.heard;
    }

    public void setHeard(Collection<Command> heard) {
        this.heard = heard;
    }

    @Nonnull
    public EntityID getID() {
        return this.entityID;
    }

    public StandardEntity me() {
        return this.worldModel.getEntity(this.getID());
    }

    public double getX() {
        return this.worldModel.getEntity(this.entityID).getLocation(this.worldModel).first();
    }

    public double getY() {
        return this.worldModel.getEntity(this.entityID).getLocation(this.worldModel).second();
    }

    public EntityID getPosition() {
        StandardEntity entity = this.worldModel.getEntity(this.getID());
        return entity instanceof Human ? ((Human) entity).getPosition() : entity.getID();
    }

    @Nonnull
    public Area getPositionArea() {
        return (Area) this.worldModel.getEntity(this.getPosition());
    }

    @Nullable
    public ChangeSet getChanged() {
        return this.changed;
    }

    public void setChanged(ChangeSet changed) {
        this.changed = changed;
    }

    @Nullable
    public Human someoneOnBoard() {

        for (StandardEntity next : this.worldModel
                .getEntitiesOfType(StandardEntityURN.CIVILIAN)) {
            Human human = (Human) next;
            if (human.getPosition().equals(this.entityID)) {
                return human;
            }
        }

        return null;
    }

    @Nullable
    public Action getExecutedAction(int time) {
        if (time > 0)
            return this.actionHistory.get(time);
        return this.actionHistory.get(this.getTime() + time);
    }


    public void setExecutedAction(int time, @Nullable Action action) {
        this.actionHistory.put(time > 0 ? time : this.getTime() + time, action);
    }

    public void recordThinkStartTime() {
        this.thinkStartTime = System.currentTimeMillis();
    }

    public long getThinkTimeMillis() {
        return (System.currentTimeMillis() - this.thinkStartTime);
    }
}
