from __future__ import annotations

from warnings import warn
from typing import TYPE_CHECKING

from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.component.module.algorithm.path_planning import (
    PathPlanning,
)

if TYPE_CHECKING:
    from rcrs_core.worldmodel.entityID import EntityID


class AStarPathPlanning(PathPlanning):
    def get_result(self) -> list[EntityID]:
        return self._result

    def get_path(
        self, from_entity_id: EntityID, to_entity_id: EntityID
    ) -> list[EntityID]:
        return []

    def get_distance(self, from_entity_id: EntityID, to_entity_id: EntityID) -> float:
        return 0.0

    def set_from(self, from_entity_id: EntityID) -> PathPlanning:
        self._from = from_entity_id
        warn("This method is deprecated. Use get_path instead.", DeprecationWarning)
        return self

    def set_destination(self, destination_entity_ids: list[EntityID]) -> PathPlanning:
        self._targets = destination_entity_ids
        warn("This method is deprecated. Use get_path instead.", DeprecationWarning)
        return self

    def calculate(self) -> AStarPathPlanning:
        warn("This method is deprecated. Use get_path instead.", DeprecationWarning)
        return self
