from __future__ import annotations

from typing import TYPE_CHECKING

from adf_core_python.core.component.module.algorithm.path_planning import (
    PathPlanning,
)

if TYPE_CHECKING:
    from rcrs_core.worldmodel.entityID import EntityID


class AStarPathPlanning(PathPlanning):
    def get_path(
        self, from_entity_id: EntityID, to_entity_id: EntityID
    ) -> list[EntityID]:
        return []

    def get_distance(self, from_entity_id: EntityID, to_entity_id: EntityID) -> float:
        return 0.0

    def calculate(self) -> AStarPathPlanning:
        return self
