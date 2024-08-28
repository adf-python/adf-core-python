from time import time
from typing import Any, Dict, List

from rcrs_core.agents.agent import Agent
from rcrs_core.entities.human import Human
from rcrs_core.worldmodel.worldmodel import ChangeSet, Entity, EntityID, WorldModel

from adf_core_python.core.agent.action.action import Action


class AgentInfo:
    # TODO: Replace Any with the actual type
    def __init__(self, agent: Agent, world_model: WorldModel):
        self._agent: Agent = agent
        self._world_model: WorldModel = world_model
        self._time: int = 0
        self._action_history: Dict[int, Action] = {}
        self._heard_commands: List[Any] = []
        self._change_set: ChangeSet = ChangeSet()
        self._start_think_time: float = 0.0

    def set_time(self, time: int) -> None:
        """
        Set the current time of the agent

        Parameters
        ----------
        time : int
            Current time
        """
        self._time = time

    def get_time(self) -> int:
        """
        Get the current time of the agent

        Returns
        -------
        int
            Current time
        """
        return self._time

    def set_heard_commands(self, heard_commands: List[Any]) -> None:
        """
        Set the heard commands

        Parameters
        ----------
        heard_commands : List[Any]
            Heard commands
        """
        self._heard_commands = heard_commands

    def get_heard_commands(self) -> List[Any]:
        """
        Get the heard commands

        Returns
        -------
        List[Any]
            Heard commands
        """
        return self._heard_commands

    def get_entity_id(self) -> EntityID:
        """
        Get the entity ID of the agent

        Returns
        -------
        EntityID
            Entity ID of the agent
        """
        return self._agent.get_id()  # type: ignore TODO: Agent class should return EntityID instead of EntityID | None

    def get_myself(self) -> Entity:
        """
        Get the entity of the agent

        Returns
        -------
        Entity
            Entity of the agent
        """
        return self._world_model.get_entity(self.get_entity_id())

    def get_position_entity_id(self) -> EntityID:
        """
        Get the position entity ID of the agent

        Returns
        -------
        EntityID
            Position entity ID of the agent
        """
        entity = self._world_model.get_entity(self.get_entity_id())
        if isinstance(entity, Human):
            return entity.get_position_property()
        else:
            return entity.get_id()

    def set_change_set(self, change_set: ChangeSet) -> None:
        """
        Set the change set

        Parameters
        ----------
        change_set : ChangeSet
            Change set
        """
        self._change_set = change_set

    def get_change_set(self) -> ChangeSet:
        """
        Get the change set

        Returns
        -------
        ChangeSet
            Change set
        """
        return self._change_set

    def some_one_on_board(self) -> Human | None:
        """
        Get the human if someone is on board

        Returns
        -------
        Human | None
            Human if someone is on board, None otherwise
        """
        entity_id: EntityID = self.get_entity_id()
        for entity in self._world_model.get_entities():
            if isinstance(entity, Human):
                if entity.get_position_property() == entity_id:
                    return entity
        return None

    def get_executed_action(self, time: int) -> Action | None:
        """
        Get the executed action at the given time

        Parameters
        ----------
        time : int
            Time
        """
        return self._action_history.get(time)

    def set_executed_action(self, time: int, action: Action) -> None:
        """
        Set the executed action at the given time

        Parameters
        ----------
        time : int
            Time
        action : Action
            Executed action
        """
        self._action_history[time] = action

    def record_think_start_time(self) -> None:
        """
        Record the start time of thinking
        """
        self._start_think_time = time()

    def get_think_time(self) -> float:
        """
        Get the time taken for thinking

        Returns
        -------
        float
            Time taken for thinking
        """
        return time() - self._start_think_time
