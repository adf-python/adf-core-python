from typing import Any

from rcrs_core.worldmodel.entityID import EntityID
from rcrs_core.worldmodel.worldmodel import WorldModel


class WorldInfo:
    def __init__(self, world_model: WorldModel):
        self._world_model: WorldModel = world_model
        self._time: int = 0
        self._is_run_rollback: bool = False
        self._rollback: dict[EntityID, dict[int, dict[int, Any]]] = {}

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
