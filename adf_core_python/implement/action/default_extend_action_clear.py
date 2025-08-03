import math
import sys
from typing import Optional, cast

from rcrscore.entities import (
    AmbulanceTeam,
    Area,
    Blockade,
    Building,
    EntityID,
    FireBrigade,
    Human,
    PoliceForce,
    Refuge,
    Road,
)
from shapely import LineString, Point, Polygon

from adf_core_python.core.agent.action.action import Action
from adf_core_python.core.agent.action.common.action_move import ActionMove
from adf_core_python.core.agent.action.common.action_rest import ActionRest
from adf_core_python.core.agent.action.police.action_clear import ActionClear
from adf_core_python.core.agent.action.police.action_clear_area import ActionClearArea
from adf_core_python.core.agent.communication.message_manager import MessageManager
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.info.agent_info import AgentInfo
from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
from adf_core_python.core.agent.info.world_info import WorldInfo
from adf_core_python.core.agent.module.module_manager import ModuleManager
from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData
from adf_core_python.core.component.action.extend_action import ExtendAction
from adf_core_python.core.component.module.algorithm.path_planning import PathPlanning


class DefaultExtendActionClear(ExtendAction):
    def __init__(
        self,
        agent_info: AgentInfo,
        world_info: WorldInfo,
        scenario_info: ScenarioInfo,
        module_manager: ModuleManager,
        develop_data: DevelopData,
    ) -> None:
        super().__init__(
            agent_info, world_info, scenario_info, module_manager, develop_data
        )
        self._clear_distance = float(
            self.scenario_info.get_value("clear.repair.distance", 0.0)
        )
        self._forced_move = float(
            develop_data.get_value(
                "adf_core_python.implement.action.DefaultExtendActionClear.forced_move",
                3,
            )
        )
        self._threshold_rest = float(
            develop_data.get_value(
                "adf_core_python.implement.action.DefaultExtendActionClear.rest", 100
            )
        )

        self._target_entity_id = None
        self._move_point_cache: dict[EntityID, Optional[set[tuple[float, float]]]] = {}
        self._old_clear_x = 0
        self._old_clear_y = 0
        self.count = 0

        self._path_planning = cast(
            PathPlanning,
            self.module_manager.get_module(
                "DefaultExtendActionClear.PathPlanning",
                "adf_core_python.implement.module.algorithm.a_star_path_planning.AStarPathPlanning",
            ),
        )

    def precompute(self, precompute_data: PrecomputeData) -> ExtendAction:
        super().precompute(precompute_data)
        if self.get_count_precompute() >= 2:
            return self
        self._path_planning.precompute(precompute_data)
        self._kernel_time = self.scenario_info.get_value("kernel.timesteps", -1)
        return self

    def resume(self, precompute_data: PrecomputeData) -> ExtendAction:
        super().resume(precompute_data)
        if self.get_count_resume() >= 2:
            return self
        self._path_planning.resume(precompute_data)
        self._kernel_time = self.scenario_info.get_value("kernel.timesteps", -1)
        return self

    def prepare(self) -> ExtendAction:
        super().prepare()
        if self.get_count_prepare() >= 2:
            return self
        self._path_planning.prepare()
        self._kernel_time = self.scenario_info.get_value("kernel.timesteps", -1)
        return self

    def update_info(self, message_manager: MessageManager) -> ExtendAction:
        super().update_info(message_manager)
        if self.get_count_update_info() >= 2:
            return self
        self._path_planning.update_info(message_manager)
        return self

    def set_target_entity_id(self, target_entity_id: EntityID) -> ExtendAction:
        self._target_entity_id = None
        target_entity = self.world_info.get_entity(target_entity_id)
        if target_entity is not None:
            if isinstance(target_entity, Road):
                self._target_entity_id = target_entity_id
            elif isinstance(target_entity, Blockade):
                self._target_entity_id = target_entity.get_position()
            elif isinstance(target_entity, Building):
                self._target_entity_id = target_entity_id
        return self

    def calculate(self) -> ExtendAction:
        self.result = None
        police_force = cast(PoliceForce, self.agent_info.get_myself())

        if self._need_rest(police_force):
            target_entity_ids: list[EntityID] = []
            if self._target_entity_id is not None:
                target_entity_ids.append(self._target_entity_id)

            self.result = self._calc_rest(
                police_force, self._path_planning, target_entity_ids
            )
            if self.result is not None:
                return self

        if self._target_entity_id is None:
            return self

        agent_position_entity_id = police_force.get_position()
        target_entity = self.world_info.get_entity(self._target_entity_id)
        position_entity = self.world_info.get_entity(agent_position_entity_id)
        if target_entity is None or isinstance(target_entity, Area) is False:
            return self
        if isinstance(position_entity, Road):
            self.result = self._get_rescue_action(
                police_force, cast(Road, position_entity)
            )
            if self.result is not None:
                return self

        if agent_position_entity_id == self._target_entity_id:
            self.result = self._get_area_clear_action(
                police_force, cast(Road, position_entity)
            )
            if self.result is not None:
                return self
        elif (
            cast(Area, target_entity).get_edge_to(agent_position_entity_id) is not None
        ):
            self.result = self._get_neighbour_position_action(
                police_force, cast(Area, target_entity)
            )
        else:
            path = self._path_planning.get_path(
                agent_position_entity_id, self._target_entity_id
            )
            if path is not None and len(path) > 0:
                index = self._index_of(path, agent_position_entity_id)
                if index == -1:
                    area = cast(Area, position_entity)
                    for i in range(0, len(path), 1):
                        if area.get_edge_to(path[i]) is not None:
                            index = i
                            break

                elif index >= 0:
                    index += 1

                if index >= 0 and index < len(path):
                    entity = self.world_info.get_entity(path[index])
                    self.result = self._get_neighbour_position_action(
                        police_force, cast(Area, entity)
                    )
                    if self.result is not None and isinstance(self.result, ActionMove):
                        action_move = cast(ActionMove, self.result)
                        if action_move.is_destination_defined():
                            self.result = None

                if self.result is None:
                    self.result = ActionMove(path)

        return self

    def _need_rest(self, police_force: PoliceForce) -> bool:
        hp = police_force.get_hp()
        damage = police_force.get_damage()

        if hp == 0 or damage == 0:
            return False

        active_time = (hp / damage) + (1 if (hp % damage) != 0 else 0)
        if self._kernel_time == -1:
            self._kernel_time = self.scenario_info.get_value("kernel.timesteps", -1)

        return damage >= self._threshold_rest or (
            active_time + self.agent_info.get_time() < self._kernel_time
        )

    def _calc_rest(
        self,
        police_force: PoliceForce,
        path_planning: PathPlanning,
        target_entity_ids: list[EntityID],
    ) -> Optional[Action]:
        position_entity_id = police_force.get_position()
        refuges = self.world_info.get_entity_ids_of_types([Refuge])
        current_size = len(refuges)
        if position_entity_id in refuges:
            return ActionRest()

        first_result: list[EntityID] = []
        while len(refuges) > 0:
            path = path_planning.get_path(position_entity_id, refuges[0])
            if path is not None and len(path) > 0:
                if first_result == []:
                    first_result = path.copy()
                    if target_entity_ids == []:
                        break

                refuge_entity_id = path[-1]
                from_refuge_to_target_path = path_planning.get_path(
                    refuge_entity_id, target_entity_ids[0]
                )
                if from_refuge_to_target_path != []:
                    return ActionMove(path)

                refuges.remove(refuge_entity_id)
                if current_size == len(refuges):
                    break
                current_size = len(refuges)
            else:
                break

        return ActionMove(first_result) if first_result != [] else None

    def _get_rescue_action(
        self, police_entity: PoliceForce, road: Road
    ) -> Optional[Action]:
        blockades = set(
            []
            if road.get_blockades() is None
            else [
                cast(Blockade, self.world_info.get_entity(blockade_entity_id))
                for blockade_entity_id in road.get_blockades()
            ]
        )
        agent_entities = set(
            self.world_info.get_entities_of_types([AmbulanceTeam, FireBrigade])
        )

        police_x = police_entity.get_x()
        police_y = police_entity.get_y()
        min_distance = sys.float_info.max
        move_action: Optional[ActionMove] = None

        for agent_entity in agent_entities:
            human = cast(Human, agent_entity)
            if human.get_position().get_value() != road.get_entity_id().get_value():
                continue

            human_x = human.get_x()
            human_y = human.get_y()
            action_clear: Optional[ActionClear | ActionClearArea] = None
            clear_blockade: Optional[Blockade] = None
            for blockade in blockades:
                if not self._is_inside(human_x, human_y, blockade.get_apexes()):
                    continue

                distance = self._get_distance(police_x, police_y, human_x, human_y)
                if self._is_intersecting_area(
                    police_x, police_y, human_x, human_y, road
                ):
                    action = self._get_intersect_edge_action(
                        police_x, police_y, human_x, human_y, road
                    )
                    if action is None:
                        continue
                    if isinstance(action, ActionClear):
                        if action_clear is None:
                            action_clear = action
                            clear_blockade = blockade
                            continue

                        if clear_blockade is not None:
                            if self._is_intersecting_blockades(
                                blockade, clear_blockade
                            ):
                                return ActionClear(clear_blockade)

                            another_distance = self.world_info.get_distance(
                                police_entity.get_entity_id(),
                                clear_blockade.get_entity_id(),
                            )
                            blockade_distance = self.world_info.get_distance(
                                police_entity.get_entity_id(), blockade.get_entity_id()
                            )
                            if blockade_distance < another_distance:
                                return action

                        return action_clear
                    elif isinstance(action, ActionMove) and distance < min_distance:
                        min_distance = distance
                        move_action = action

                    elif self._is_intersecting_blockade(
                        police_x, police_y, human_x, human_y, blockade
                    ):
                        vector = self._scale_clear(
                            self._get_vector(police_x, police_y, human_x, human_y)
                        )
                        clear_x = int(police_x + vector[0])
                        clear_y = int(police_y + vector[1])

                        vector = self._scale_back_clear(vector)
                        start_x = int(police_x + vector[0])
                        start_y = int(police_y + vector[1])

                        if self._is_intersecting_blockade(
                            start_x, start_y, clear_x, clear_y, blockade
                        ):
                            if action_clear is None:
                                action_clear = ActionClearArea(clear_x, clear_y)
                                clear_blockade = blockade
                            else:
                                if clear_blockade is not None:
                                    if self._is_intersecting_blockades(
                                        blockade, clear_blockade
                                    ):
                                        return ActionClear(clear_blockade)

                                    distance1 = self.world_info.get_distance(
                                        police_entity.get_entity_id(),
                                        clear_blockade.get_entity_id(),
                                    )
                                    distance2 = self.world_info.get_distance(
                                        police_entity.get_entity_id(),
                                        blockade.get_entity_id(),
                                    )
                                    if distance1 > distance2:
                                        return ActionClearArea(clear_x, clear_y)

                                return action_clear

                        elif distance < min_distance:
                            min_distance = distance
                            move_action = ActionMove(
                                [road.get_entity_id()], human_x, human_y
                            )

                if action_clear is not None:
                    return action_clear

        return move_action

    def _is_inside(self, x: float, y: float, apexes: list[int]) -> bool:
        point = Point(x, y)
        polygon = Polygon(
            [(apexes[i], apexes[i + 1]) for i in range(0, len(apexes), 2)]
        )
        return polygon.contains(point)

    def _get_distance(self, x1: float, y1: float, x2: float, y2: float) -> float:
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def _is_intersecting_area(
        self, agent_x: float, agent_y: float, point_x: float, point_y: float, area: Area
    ) -> bool:
        for edge in area.get_edges():
            start_x = edge.get_start_x()
            start_y = edge.get_start_y()
            end_x = edge.get_end_x()
            end_y = edge.get_end_y()

            line1 = LineString([(agent_x, agent_y), (point_x, point_y)])
            line2 = LineString([(start_x, start_y), (end_x, end_y)])
            if line1.intersects(line2):
                mid_x = (start_x + end_x) / 2.0
                mid_y = (start_y + end_y) / 2.0
                if not self._equals_point(
                    agent_x, agent_y, mid_x, mid_y, 1000
                ) and not self._equals_point(point_x, point_y, mid_x, mid_y, 1000):
                    return True

        return False

    def _equals_point(
        self, x1: float, y1: float, x2: float, y2: float, range: float
    ) -> bool:
        return (x2 - range < x1 and x1 < x2 + range) and (
            y2 - range < y1 and y1 < y2 + range
        )

    def _get_intersect_edge_action(
        self, agent_x: float, agent_y: float, point_x: float, point_y: float, road: Road
    ) -> Action:
        move_points = self._get_move_points(road)
        best_point: Optional[tuple[float, float]] = None
        best_distance = sys.float_info.max
        for point in move_points:
            if not self._is_intersecting_area(
                agent_x, agent_y, point[0], point[1], road
            ):
                if not self._is_intersecting_area(
                    point_x, point_y, point[0], point[1], road
                ):
                    distance = self._get_distance(point_x, point_y, point[0], point[1])
                    if distance < best_distance:
                        best_point = point
                        best_distance = distance

        if best_point is not None:
            bp_x, bp_y = best_point
            if road.get_blockades() is None:
                return ActionMove([road.get_entity_id()], int(bp_x), int(bp_y))

            action_clear: Optional[ActionClearArea] = None
            clear_blockade: Optional[Blockade] = None
            action_move: Optional[ActionMove] = None

            vector = self._scale_clear(self._get_vector(agent_x, agent_y, bp_x, bp_y))
            clear_x = int(agent_x + vector[0])
            clear_y = int(agent_x + vector[1])

            vector = self._scale_back_clear(vector)
            start_x = int(agent_x + vector[0])
            start_y = int(agent_y + vector[1])

            for blockade in self.world_info.get_blockades(road):
                if self._is_intersecting_blockade(
                    start_x, start_y, bp_x, bp_y, blockade
                ):
                    if self._is_intersecting_blockade(
                        start_x, start_y, clear_x, clear_y, blockade
                    ):
                        if action_clear is None:
                            action_clear = ActionClearArea(clear_x, clear_y)
                            clear_blockade = blockade
                        else:
                            if (
                                clear_blockade is not None
                                and self._is_intersecting_blockades(
                                    blockade, clear_blockade
                                )
                            ):
                                return ActionClear(clear_blockade)
                            return action_clear
                    elif action_move is None:
                        action_move = ActionMove(
                            [road.get_entity_id()], int(bp_x), int(bp_y)
                        )

            if action_clear is not None:
                return action_clear
            if action_move is not None:
                return action_move

        action = self._get_area_clear_action(
            cast(PoliceForce, self.agent_info.get_myself()), road
        )
        if action is None:
            action = ActionMove([road.get_entity_id()], int(point_x), int(point_y))
        return action

    def _get_move_points(self, road: Road) -> set[tuple[float, float]]:
        points: Optional[set[tuple[float, float]]] = self._move_point_cache.get(
            road.get_entity_id()
        )
        if points is None:
            points = set()
            apex = road.get_apexes()
            for i in range(0, len(apex), 2):
                for j in range(i + 2, len(apex), 2):
                    mid_x = (apex[i] + apex[j]) / 2.0
                    mid_y = (apex[i + 1] + apex[j + 1]) / 2.0
                    if self._is_inside(mid_x, mid_y, apex):
                        points.add((mid_x, mid_y))

            for edge in road.get_edges():
                mid_x = (edge.get_start_x() + edge.get_end_x()) / 2.0
                mid_y = (edge.get_start_y() + edge.get_end_y()) / 2.0
                if (mid_x, mid_y) in points:
                    points.remove((mid_x, mid_y))

            self._move_point_cache[road.get_entity_id()] = points

        return points

    def _get_vector(
        self, from_x: float, from_y: float, to_x: float, to_y: float
    ) -> tuple[float, float]:
        return (to_x - from_x, to_y - from_y)

    def _scale_clear(self, vector: tuple[float, float]) -> tuple[float, float]:
        length = 1.0 / math.hypot(vector[0], vector[1])
        return (
            vector[0] * length * self._clear_distance,
            vector[1] * length * self._clear_distance,
        )

    def _scale_back_clear(self, vector: tuple[float, float]) -> tuple[float, float]:
        length = 1.0 / math.hypot(vector[0], vector[1])
        return (vector[0] * length * -510, vector[1] * length * -510)

    def _is_intersecting_blockade(
        self,
        agent_x: float,
        agent_y: float,
        point_x: float,
        point_y: float,
        blockade: Blockade,
    ) -> bool:
        apexes = blockade.get_apexes()
        for i in range(0, len(apexes) - 3, 2):
            line1 = LineString(
                [(apexes[i], apexes[i + 1]), (apexes[i + 2], apexes[i + 3])]
            )
            line2 = LineString([(agent_x, agent_y), (point_x, point_y)])
            if line1.intersects(line2):
                return True
        return False

    def _is_intersecting_blockades(
        self, blockade1: Blockade, blockade2: Blockade
    ) -> bool:
        apexes1 = blockade1.get_apexes()
        apexes2 = blockade2.get_apexes()
        for i in range(0, len(apexes1) - 2, 2):
            for j in range(0, len(apexes2) - 2, 2):
                line1 = LineString(
                    [(apexes1[i], apexes1[i + 1]), (apexes1[i + 2], apexes1[i + 3])]
                )
                line2 = LineString(
                    [(apexes2[j], apexes2[j + 1]), (apexes2[j + 2], apexes2[j + 3])]
                )
                if line1.intersects(line2):
                    return True

        for i in range(0, len(apexes1) - 2, 2):
            line1 = LineString(
                [(apexes1[i], apexes1[i + 1]), (apexes1[i + 2], apexes1[i + 3])]
            )
            line2 = LineString([(apexes2[-2], apexes2[-1]), (apexes2[0], apexes2[1])])
            if line1.intersects(line2):
                return True

        for i in range(0, len(apexes2) - 2, 2):
            line1 = LineString([(apexes1[-2], apexes1[-1]), (apexes1[0], apexes1[1])])
            line2 = LineString(
                [(apexes2[i], apexes2[i + 1]), (apexes2[i + 2], apexes2[i + 3])]
            )
            if line1.intersects(line2):
                return True

        return False

    def _get_area_clear_action(
        self, police_entity: PoliceForce, road: Road
    ) -> Optional[Action]:
        if road.get_blockades() == []:
            return None

        blockades = set(self.world_info.get_blockades(road))
        min_distance = sys.float_info.max
        clear_blockade: Optional[Blockade] = None
        for blockade in blockades:
            for another in blockades:
                if blockade == another:
                    continue

                if self._is_intersecting_blockades(blockade, another):
                    distance1 = self.world_info.get_distance(
                        police_entity.get_entity_id(), blockade.get_entity_id()
                    )
                    distance2 = self.world_info.get_distance(
                        police_entity.get_entity_id(), another.get_entity_id()
                    )
                    if distance1 <= distance2 and distance1 < min_distance:
                        min_distance = distance1
                        clear_blockade = blockade
                    elif distance2 < min_distance:
                        min_distance = distance2
                        clear_blockade = another

        if clear_blockade is not None:
            if min_distance < self._clear_distance:
                return ActionClear(clear_blockade)
            else:
                return ActionMove(
                    [police_entity.get_position()],
                    clear_blockade.get_x(),
                    clear_blockade.get_y(),
                )

        agent_x = police_entity.get_x()
        agent_y = police_entity.get_y()
        clear_blockade = None
        min_point_distance = sys.float_info.max
        clear_x = 0
        clear_y = 0
        for blockade in blockades:
            apexes = blockade.get_apexes()
            for i in range(0, len(apexes) - 2, 2):
                distance = self._get_distance(
                    agent_x, agent_y, apexes[i], apexes[i + 1]
                )
                if distance < min_point_distance:
                    clear_blockade = blockade
                    min_point_distance = distance
                    clear_x = apexes[i]
                    clear_y = apexes[i + 1]

        if clear_blockade is not None:
            if min_point_distance < self._clear_distance:
                vector = self._scale_clear(
                    self._get_vector(agent_x, agent_y, clear_x, clear_y)
                )
                clear_x = int(agent_x + vector[0])
                clear_y = int(agent_y + vector[1])
                return ActionClearArea(clear_x, clear_y)
            return ActionMove([police_entity.get_position()], clear_x, clear_y)

        return None

    def _index_of(self, list: list[EntityID], x: EntityID) -> int:
        return list.index(x) if x in list else -1

    def _get_neighbour_position_action(
        self, police_entity: PoliceForce, target: Area
    ) -> Optional[Action]:
        agent_x = police_entity.get_x()
        agent_y = police_entity.get_y()
        position = self.world_info.get_entity(police_entity.get_position())
        if position is None:
            return None

        edge = target.get_edge_to(position.get_entity_id())
        if edge is None:
            return None

        if isinstance(position, Road):
            road = cast(Road, position)
            if road.get_blockades() != []:
                mid_x = (edge.get_start_x() + edge.get_end_x()) / 2.0
                mid_y = (edge.get_start_y() + edge.get_end_y()) / 2.0
                if self._is_intersecting_area(agent_x, agent_y, mid_x, mid_y, road):
                    return self._get_intersect_edge_action(
                        agent_x, agent_y, mid_x, mid_y, road
                    )

                action_clear: Optional[ActionClear | ActionClearArea] = None
                clear_blockade: Optional[Blockade] = None
                action_move: Optional[ActionMove] = None

                vector = self._scale_clear(
                    self._get_vector(agent_x, agent_y, mid_x, mid_y)
                )
                clear_x = int(agent_x + vector[0])
                clear_y = int(agent_y + vector[1])

                vector = self._scale_back_clear(vector)
                start_x = int(agent_x + vector[0])
                start_y = int(agent_y + vector[1])

                for blockade in self.world_info.get_blockades(road):
                    if self._is_intersecting_blockade(
                        start_x, start_y, mid_x, mid_y, blockade
                    ):
                        if self._is_intersecting_blockade(
                            start_x, start_y, clear_x, clear_y, blockade
                        ):
                            if action_clear is None:
                                action_clear = ActionClearArea(clear_x, clear_y)
                                clear_blockade = blockade
                                if self._equals_point(
                                    self._old_clear_x,
                                    self._old_clear_y,
                                    clear_x,
                                    clear_y,
                                    1000,
                                ):
                                    if self.count >= self._forced_move:
                                        self.count = 0
                                        return ActionMove(
                                            [road.get_entity_id()],
                                            int(clear_x),
                                            int(clear_y),
                                        )
                                    self.count += 1

                                self._old_clear_x = clear_x
                                self._old_clear_y = clear_y
                            else:
                                if clear_blockade is not None:
                                    if self._is_intersecting_blockades(
                                        blockade, clear_blockade
                                    ):
                                        return ActionClear(clear_blockade)

                                return action_clear
                        elif action_move is None:
                            action_move = ActionMove(
                                [road.get_entity_id()], int(mid_x), int(mid_y)
                            )

                if action_clear is not None:
                    return action_clear
                if action_move is not None:
                    return action_move

        if isinstance(target, Road):
            road = cast(Road, target)
            if road.get_blockades() == []:
                return ActionMove([position.get_entity_id(), target.get_entity_id()])

            target_blockade: Optional[Blockade] = None
            min_point_distance = sys.float_info.max
            clear_x = 0
            clear_y = 0
            for blockade in self.world_info.get_blockades(road):
                apexes = blockade.get_apexes()
                for i in range(0, len(apexes) - 2, 2):
                    distance = self._get_distance(
                        agent_x, agent_y, apexes[i], apexes[i + 1]
                    )
                    if distance < min_point_distance:
                        target_blockade = blockade
                        min_point_distance = distance
                        clear_x = apexes[i]
                        clear_y = apexes[i + 1]

            if (
                target_blockade is not None
                and min_point_distance < self._clear_distance
            ):
                vector = self._scale_clear(
                    self._get_vector(agent_x, agent_y, clear_x, clear_y)
                )
                clear_x = int(agent_x + vector[0])
                clear_y = int(agent_y + vector[1])
                if self._equals_point(
                    self._old_clear_x, self._old_clear_y, clear_x, clear_y, 1000
                ):
                    if self.count >= self._forced_move:
                        self.count = 0
                        return ActionMove([road.get_entity_id()], clear_x, clear_y)
                    self.count += 1

                self._old_clear_x = clear_x
                self._old_clear_y = clear_y
                return ActionClearArea(clear_x, clear_y)

        return ActionMove([position.get_entity_id(), target.get_entity_id()])
