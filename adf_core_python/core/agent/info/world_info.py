from typing import Any, Optional

from rcrs_core.entities.entity import Entity
from rcrs_core.worldmodel.changeSet import ChangeSet
from rcrs_core.worldmodel.entityID import EntityID
from rcrs_core.worldmodel.worldmodel import WorldModel


class WorldInfo:
    def __init__(self, world_model: WorldModel):
        self._world_model: WorldModel = world_model
        self._time: int = 0
        self._is_run_rollback: bool = False
        self._rollback: dict[EntityID, dict[int, dict[int, Any]]] = {}
        self._change_set: ChangeSet

    # TODO: Implement the worldmodel access methods
    def get_world_model(self) -> WorldModel:
        """
        Get the world model

        Returns
        -------
        WorldModel
            World model
        """
        return self._world_model

    def set_change_set(self, change_set: ChangeSet) -> None:
        """
        Set the change set

        Parameters
        ----------
        change_set : ChangeSet
            Change set
        """
        self._change_set = change_set

    def get_entity(self, entity_id: EntityID) -> Optional[Entity]:
        """
        Get the entity

        Parameters
        ----------
        entity_id : EntityID
            Entity ID

        Returns
        -------
        Optional[Entity]
            Entity
        """
        return self._world_model.get_entity(entity_id)

    def get_entity_ids_of_type(self, entity_type: type[Entity]) -> list[EntityID]:
        """
        Get the entity IDs of the specified type

        Parameters
        ----------
        entity_type : type[Entity]
            Entity type

        Returns
        -------
        list[EntityID]
            Entity IDs
        """
        entity_ids: list[EntityID] = []
        for entity in self._world_model.get_entities():
            if isinstance(entity, entity_type):
                entity_ids.append(entity.get_id())

        return entity_ids
    
    def get_entities_of_type(self, entity_type: type[Entity]) -> list[Entity]:
        """
        Get the entities of the specified type

        Parameters
        ----------
        entity_type : type[Entity]
            Entity type

        Returns
        -------
        list[Entity]
            Entities
        """
        entities: list[Entity] = []
        for entity in self._world_model.get_entities():
            if isinstance(entity, entity_type):
                entities.append(entity)

        return entities
