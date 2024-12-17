from typing import Optional, cast

from rcrs_core.entities.ambulanceTeam import AmbulanceTeam
from rcrs_core.entities.area import Area
from rcrs_core.entities.civilian import Civilian
from rcrs_core.entities.human import Human
from rcrs_core.entities.refuge import Refuge
from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.action.common.action_move import ActionMove
from adf_core_python.core.agent.action.common.action_rest import ActionRest
from adf_core_python.core.agent.communication.message_manager import MessageManager
from adf_core_python.core.agent.communication.standard.bundle.centralized.command_ambulance import (
    CommandAmbulance,
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


class DefaultCommandExecutorAmbulance(CommandExecutor):
    ACTION_UNKNOWN: int = -1
    ACTION_REST = CommandAmbulance.ACTION_REST
    ACTION_MOVE = CommandAmbulance.ACTION_MOVE
    ACTION_RESCUE = CommandAmbulance.ACTION_RESCUE
    ACTION_LOAD = CommandAmbulance.ACTION_LOAD
    ACTION_UNLOAD = CommandAmbulance.ACTION_UNLOAD
    ACTION_AUTONOMY = CommandAmbulance.ACTION_AUTONOMY

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
        self._command_type = self.ACTION_UNKNOWN

        self._path_planning: PathPlanning = cast(
            PathPlanning,
            module_manager.get_module(
                "DefaultCommandExecutorAmbulance.PathPlanning",
                "adf_core_python.implement.module.algorithm.a_star_path_planning.AStarPathPlanning",
            ),
        )
        self._action_transport = module_manager.get_extend_action(
            "DefaultCommandExecutorAmbulance.ExtActionTransport",
            "adf_core_python.implement.action.default_extend_action_transport.DefaultExtendActionTransport",
        )
        self._action_move = module_manager.get_extend_action(
            "DefaultCommandExecutorAmbulance.ExtActionMove",
            "adf_core_python.implement.action.default_extend_action_move.DefaultExtendActionMove",
        )

        self._command_type: int = self.ACTION_UNKNOWN
        self._target: Optional[EntityID] = None
        self._commander: Optional[EntityID] = None

    def set_command(self, command: CommandAmbulance) -> CommandExecutor:
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
            case self.ACTION_RESCUE:
                if self._target:
                    self._result = (
                        self._action_move.set_target_entity_id(self._target)
                        .calculate()
                        .get_action()
                    )
                return self
            case self.ACTION_LOAD:
                if self._target:
                    self._result = (
                        self._action_move.set_target_entity_id(self._target)
                        .calculate()
                        .get_action()
                    )
                return self
            case self.ACTION_UNLOAD:
                if self._target:
                    self._result = (
                        self._action_move.set_target_entity_id(self._target)
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
                            self._action_transport.set_target_entity_id(self._target)
                            .calculate()
                            .get_action()
                        )
                elif isinstance(target_entity, Human):
                    self._result = (
                        self._action_transport.set_target_entity_id(self._target)
                        .calculate()
                        .get_action()
                    )
        return self

    def update_info(self, message_manager: MessageManager) -> CommandExecutor:
        super().update_info(message_manager)
        if self.get_count_update_info() >= 2:
            return self

        self._path_planning.update_info(message_manager)
        self._action_transport.update_info(message_manager)
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

            if self._command_type == self.ACTION_LOAD:
                self._command_type = self.ACTION_UNLOAD
                self._target = None
            else:
                self._command_type = self.ACTION_UNKNOWN
                self._target = None
                self._commander = None

        return self

    def precompute(self, precompute_data: PrecomputeData) -> CommandExecutor:
        super().precompute(precompute_data)
        if self.get_count_precompute() >= 2:
            return self
        self._path_planning.precompute(precompute_data)
        self._action_transport.precompute(precompute_data)
        self._action_move.precompute(precompute_data)
        return self

    def resume(self, precompute_data: PrecomputeData) -> CommandExecutor:
        super().resume(precompute_data)
        if self.get_count_resume() >= 2:
            return self
        self._path_planning.resume(precompute_data)
        self._action_transport.resume(precompute_data)
        self._action_move.resume(precompute_data)
        return self

    def prepare(self) -> CommandExecutor:
        super().prepare()
        if self.get_count_prepare() >= 2:
            return self
        self._path_planning.prepare()
        self._action_transport.prepare()
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
            case self.ACTION_RESCUE:
                if self._target is None:
                    return True
                human = self._world_info.get_entity(self._target)
                if not isinstance(human, Human):
                    return True
                return human.get_buriedness() == 0 or human.get_hp() == 0
            case self.ACTION_LOAD:
                if self._target is None:
                    return True
                human = self._world_info.get_entity(self._target)
                if not isinstance(human, Human):
                    return True
                if human.get_hp() == 0:
                    return True
                if isinstance(human, Civilian):
                    self._command_type = self.ACTION_RESCUE
                    return self._is_command_completed()
                if human.get_position() is not None:
                    position = human.get_position()
                    if position in self._world_info.get_entity_ids_of_types(
                        [AmbulanceTeam]
                    ):
                        return True
                    elif isinstance(self._world_info.get_entity(position), Refuge):
                        return True
                return False

            case self.ACTION_UNLOAD:
                if self._target is not None:
                    entity = self._world_info.get_entity(self._target)
                    if entity is not None and isinstance(entity, Refuge):
                        if self._target == self._agent_info.get_position_entity_id():
                            return False
                return self._agent_info.some_one_on_board() is None
            case self.ACTION_AUTONOMY:
                if self._target is not None:
                    target_entity = self._world_info.get_entity(self._target)
                    if isinstance(target_entity, Area):
                        self._command_type = (
                            self._agent_info.some_one_on_board() is None
                            and self.ACTION_MOVE
                            or self.ACTION_UNLOAD
                        )
                        return self._is_command_completed()
                    elif isinstance(target_entity, Human):
                        human = target_entity
                        if human.get_hp() == 0:
                            return True
                        self._command_type = (
                            isinstance(human, Civilian)
                            and self.ACTION_LOAD
                            or self.ACTION_RESCUE
                        )
                        return self._is_command_completed()
                return True
            case _:
                return True
