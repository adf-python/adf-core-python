from typing import Optional, cast

from rcrs_core.entities.area import Area
from rcrs_core.entities.blockade import Blockade
from rcrs_core.entities.human import Human
from rcrs_core.entities.refuge import Refuge
from rcrs_core.entities.road import Road
from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.action.common.action_move import ActionMove
from adf_core_python.core.agent.action.common.action_rest import ActionRest
from adf_core_python.core.agent.communication.message_manager import MessageManager
from adf_core_python.core.agent.communication.standard.bundle.centralized.command_police import (
    CommandPolice,
)
from adf_core_python.core.agent.communication.standard.bundle.centralized.message_report import (
    MessageReport,
)
from adf_core_python.core.agent.communication.standard.bundle.standard_message_priority import (
    StandardMessagePriority,
)
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.info.agent_info import AgentInfo
from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
from adf_core_python.core.agent.info.world_info import WorldInfo
from adf_core_python.core.agent.module.module_manager import ModuleManager
from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData
from adf_core_python.core.component.centralized.command_executor import CommandExecutor
from adf_core_python.core.component.module.algorithm.path_planning import PathPlanning


class DefaultCommandExecutorPolice(CommandExecutor):
    ACTION_UNKNOWN: int = -1
    ACTION_REST = CommandPolice.ACTION_REST
    ACTION_MOVE = CommandPolice.ACTION_MOVE
    ACTION_CLEAR = CommandPolice.ACTION_CLEAR
    ACTION_AUTONOMY = CommandPolice.ACTION_AUTONOMY

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

        self._path_planning: PathPlanning = cast(
            PathPlanning,
            module_manager.get_module(
                "DefaultCommandExecutorPolice.PathPlanning",
                "adf_core_python.implement.module.algorithm.a_star_path_planning.AStarPathPlanning",
            ),
        )
        self._action_clear = module_manager.get_extend_action(
            "DefaultCommandExecutorPolice.ExtActionClear",
            "adf_core_python.implement.action.default_extend_action_clear.DefaultExtendActionClear",
        )
        self._action_move = module_manager.get_extend_action(
            "DefaultCommandExecutorPolice.ExtActionMove",
            "adf_core_python.implement.action.default_extend_action_move.DefaultExtendActionMove",
        )

        self._command_type: int = self.ACTION_UNKNOWN
        self._target: Optional[EntityID] = None
        self._commander: Optional[EntityID] = None

    def set_command(self, command: CommandPolice) -> CommandExecutor:
        agent_id: EntityID = self._agent_info.get_entity_id()
        if command.get_command_executor_agent_entity_id() != agent_id:
            return self

        self._command_type = command.get_execute_action() or self.ACTION_UNKNOWN
        self._target = command.get_command_target_entity_id()
        self._commander = command.get_sender_entity_id()
        return self

    def calculate(self) -> CommandExecutor:
        self._result = None
        match self._command_type:
            case self.ACTION_REST:
                position = self._agent_info.get_entity_id()
                if self._target is None:
                    refuges = self._world_info.get_entity_ids_of_types([Refuge])
                    if position in refuges:
                        self._result = ActionRest()
                    else:
                        path = self._path_planning.get_path(position, refuges[0])
                        if path:
                            self._result = ActionMove(path)
                        else:
                            self._result = ActionRest()
                    return self
                if position != self._target:
                    path = self._path_planning.get_path(position, self._target)
                    if path:
                        self._result = ActionMove(path)
                        return self
                self._result = ActionRest()
                return self
            case self.ACTION_MOVE:
                if self._target:
                    self._result = (
                        self._action_move.set_target_entity_id(self._target)
                        .calculate()
                        .get_action()
                    )
                return self
            case self.ACTION_CLEAR:
                if self._target:
                    self._result = (
                        self._action_clear.set_target_entity_id(self._target)
                        .calculate()
                        .get_action()
                    )
                return self
            case self.ACTION_AUTONOMY:
                if self._target is None:
                    return self
                target_entity = self._world_info.get_entity(self._target)
                if isinstance(target_entity, Area):
                    if self._agent_info.some_one_on_board() is None:
                        self._result = (
                            self._action_move.set_target_entity_id(self._target)
                            .calculate()
                            .get_action()
                        )
                    else:
                        self._result = (
                            self._action_move.set_target_entity_id(self._target)
                            .calculate()
                            .get_action()
                        )
                elif isinstance(target_entity, Human):
                    self._result = (
                        self._action_clear.set_target_entity_id(self._target)
                        .calculate()
                        .get_action()
                    )
        return self

    def update_info(self, message_manager: MessageManager) -> CommandExecutor:
        super().update_info(message_manager)
        if self.get_count_update_info() >= 2:
            return self

        self._path_planning.update_info(message_manager)
        self._action_clear.update_info(message_manager)
        self._action_move.update_info(message_manager)

        if self._is_command_completed():
            if self._command_type == self.ACTION_UNKNOWN:
                return self
            if self._commander is None:
                return self

            message_manager.add_message(
                MessageReport(
                    True,
                    True,
                    False,
                    self._commander,
                    StandardMessagePriority.NORMAL,
                )
            )
            self._command_type = self.ACTION_UNKNOWN
            self._target = None
            self._commander = None

        return self

    def precompute(self, precompute_data: PrecomputeData) -> CommandExecutor:
        super().precompute(precompute_data)
        if self.get_count_precompute() >= 2:
            return self
        self._path_planning.precompute(precompute_data)
        self._action_clear.precompute(precompute_data)
        self._action_move.precompute(precompute_data)
        return self

    def resume(self, precompute_data: PrecomputeData) -> CommandExecutor:
        super().resume(precompute_data)
        if self.get_count_resume() >= 2:
            return self
        self._path_planning.resume(precompute_data)
        self._action_clear.resume(precompute_data)
        self._action_move.resume(precompute_data)
        return self

    def prepare(self) -> CommandExecutor:
        super().prepare()
        if self.get_count_prepare() >= 2:
            return self
        self._path_planning.prepare()
        self._action_clear.prepare()
        self._action_move.prepare()
        return self

    def _is_command_completed(self) -> bool:
        agent = self._agent_info.get_myself()
        if not isinstance(agent, Human):
            return False

        match self._command_type:
            case self.ACTION_REST:
                if self._target is None:
                    return agent.get_damage() == 0
                if (target_entity := self._world_info.get_entity(self._target)) is None:
                    return False
                if isinstance(target_entity, Refuge):
                    return agent.get_damage() == 0
                return False
            case self.ACTION_MOVE:
                return (
                    self._target is None
                    or self._agent_info.get_position_entity_id() == self._target
                )
            case self.ACTION_CLEAR:
                if self._target is None:
                    return True
                entity = self._world_info.get_entity(self._target)
                if isinstance(entity, Road):
                    if entity.get_blockades is not None:
                        return len(entity.get_blockades()) == 0
                    return self._agent_info.get_position_entity_id() == self._target
                return True
            case self.ACTION_AUTONOMY:
                if self._target is not None:
                    target_entity = self._world_info.get_entity(self._target)
                    if isinstance(target_entity, Refuge):
                        self._command_type = (
                            self.ACTION_REST
                            if agent.get_damage() > 0
                            else self.ACTION_CLEAR
                        )
                        return self._is_command_completed()
                    elif isinstance(target_entity, Area):
                        self._command_type = self.ACTION_CLEAR
                        return self._is_command_completed()
                    elif isinstance(target_entity, Human):
                        if target_entity.get_hp() == 0:
                            return True
                        if target_entity.get_position() is not None and isinstance(
                            self._world_info.get_entity(target_entity.get_position()),
                            Area,
                        ):
                            self._target = target_entity.get_position()
                            self._command_type = self.ACTION_CLEAR
                            return self._is_command_completed()
                        elif isinstance(target_entity, Blockade):
                            if target_entity.get_position() is not None:
                                self._target = target_entity.get_position()
                                self._command_type = self.ACTION_CLEAR
                                return self._is_command_completed()
                return True
            case _:
                return True
