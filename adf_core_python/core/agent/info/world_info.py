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

    def get_entity_ids_of_types(
        self, entity_types: list[type[Entity]]
    ) -> list[EntityID]:
        """
        Get the entity IDs of the specified types

        Parameters
        ----------
        entity_types : list[type[Entity]]
            List of entity types

        Returns
        -------
        list[EntityID]
            Entity IDs
        """
        entity_ids: list[EntityID] = []
        for entity in self._world_model.get_entities():
            if any(isinstance(entity, entity_type) for entity_type in entity_types):
                entity_ids.append(entity.get_id())

        return entity_ids

    def get_entities_of_types(self, entity_types: list[type[Entity]]) -> list[Entity]:
        """
        Get the entities of the specified types

        Parameters
        ----------
        entity_types : list[type[Entity]]
            List of entity types

        Returns
        -------
        list[Entity]
            Entities
        """
        entities: list[Entity] = []
        for entity in self._world_model.get_entities():
            if any(isinstance(entity, entity_type) for entity_type in entity_types):
                entities.append(entity)

        return entities

    def get_distance(self, entity_id1: EntityID, entity_id2: EntityID) -> float:
        """
        Get the distance between two entities

        Parameters
        ----------
        entity_id1 : EntityID
            Entity ID 1
        entity_id2 : EntityID
            Entity ID 2

        Returns
        -------
        float
            Distance

        Raises
        ------
        ValueError
            If one or both entities are invalid or the location is invalid
        """
        entity1: Optional[Entity] = self.get_entity(entity_id1)
        entity2: Optional[Entity] = self.get_entity(entity_id2)
        if entity1 is None or entity2 is None:
            raise ValueError(
                f"One or both entities are invalid: entity_id1={entity_id1}, entity_id2={entity_id2}, entity1={entity1}, entity2={entity2}"
            )

        location1_x, location1_y = entity1.get_location()
        location2_x, location2_y = entity2.get_location()
        if (
            location1_x is None
            or location1_y is None
            or location2_x is None
            or location2_y is None
        ):
            raise ValueError(
                f"Invalid location: entity_id1={entity_id1}, entity_id2={entity_id2}, location1_x={location1_x}, location1_y={location1_y}, location2_x={location2_x}, location2_y={location2_y}"
            )

        distance: float = (
            (location1_x - location2_x) ** 2 + (location1_y - location2_y) ** 2
        ) ** 0.5

        return distance

    def get_change_set(self) -> ChangeSet:
        """
        Get the change set

        Returns
        -------
        ChangeSet
            Change set
        """
        return self._change_set
