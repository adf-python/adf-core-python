import sys
import time as _time
from abc import abstractmethod
from threading import Event
from typing import Any, Callable, NoReturn

from bitarray import bitarray
from rcrs_core.commands.AKClear import AKClear
from rcrs_core.commands.AKClearArea import AKClearArea
from rcrs_core.commands.AKLoad import AKLoad
from rcrs_core.commands.AKMove import AKMove
from rcrs_core.commands.AKRescue import AKRescue
from rcrs_core.commands.AKRest import AKRest
from rcrs_core.commands.AKSay import AKSay
from rcrs_core.commands.AKSpeak import AKSpeak
from rcrs_core.commands.AKSubscribe import AKSubscribe
from rcrs_core.commands.AKTell import AKTell
from rcrs_core.commands.AKUnload import AKUnload
from rcrs_core.commands.Command import Command
from rcrs_core.config.config import Config as RCRSConfig
from rcrs_core.connection.URN import Command as CommandURN
from rcrs_core.connection.URN import ComponentCommand as ComponentCommandMessageID
from rcrs_core.connection.URN import ComponentControlMSG as ComponentControlMessageID
from rcrs_core.connection.URN import Entity as EntityURN
from rcrs_core.messages.AKAcknowledge import AKAcknowledge
from rcrs_core.messages.AKConnect import AKConnect
from rcrs_core.messages.controlMessageFactory import ControlMessageFactory
from rcrs_core.messages.KAConnectError import KAConnectError
from rcrs_core.messages.KAConnectOK import KAConnectOK
from rcrs_core.messages.KASense import KASense
from rcrs_core.worldmodel.changeSet import ChangeSet
from rcrs_core.worldmodel.entityID import EntityID
from rcrs_core.worldmodel.worldmodel import WorldModel

from adf_core_python.core.agent.communication.message_manager import MessageManager
from adf_core_python.core.agent.communication.standard.bundle.centralized.command_ambulance import (
    CommandAmbulance,
)
from adf_core_python.core.agent.communication.standard.bundle.centralized.command_fire import (
    CommandFire,
)
from adf_core_python.core.agent.communication.standard.bundle.centralized.command_police import (
    CommandPolice,
)
from adf_core_python.core.agent.communication.standard.bundle.centralized.command_scout import (
    CommandScout,
)
from adf_core_python.core.agent.communication.standard.bundle.centralized.message_report import (
    MessageReport,
)
from adf_core_python.core.agent.communication.standard.bundle.information.message_ambulance_team import (
    MessageAmbulanceTeam,
)
from adf_core_python.core.agent.communication.standard.bundle.information.message_building import (
    MessageBuilding,
)
from adf_core_python.core.agent.communication.standard.bundle.information.message_civilian import (
    MessageCivilian,
)
from adf_core_python.core.agent.communication.standard.bundle.information.message_fire_brigade import (
    MessageFireBrigade,
)
from adf_core_python.core.agent.communication.standard.bundle.information.message_police_force import (
    MessagePoliceForce,
)
from adf_core_python.core.agent.communication.standard.bundle.information.message_road import (
    MessageRoad,
)
from adf_core_python.core.agent.communication.standard.standard_communication_module import (
    StandardCommunicationModule,
)
from adf_core_python.core.agent.config.module_config import ModuleConfig
from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.info.agent_info import AgentInfo
from adf_core_python.core.agent.info.scenario_info import Mode, ScenarioInfo
from adf_core_python.core.agent.info.world_info import WorldInfo
from adf_core_python.core.agent.precompute.precompute_data import PrecomputeData
from adf_core_python.core.component.communication.communication_module import (
    CommunicationModule,
)
from adf_core_python.core.config.config import Config
from adf_core_python.core.launcher.config_key import ConfigKey
from adf_core_python.core.logger.logger import get_agent_logger, get_logger


class Agent:
    def __init__(
        self,
        is_precompute: bool,
        name: str,
        is_debug: bool,
        team_name: str,
        data_storage_name: str,
        module_config: ModuleConfig,
        develop_data: DevelopData,
        finish_post_connect_event: Event,
    ) -> None:
        self.name = name
        self.connect_request_id = None
        self.world_model = WorldModel()
        self.config: Config
        self.random = None
        self.agent_id: EntityID
        self.precompute_flag = is_precompute
        self.logger = get_logger(
            f"{self.__class__.__module__}.{self.__class__.__qualname__}"
        )
        self.finish_post_connect_event = finish_post_connect_event

        self.team_name = team_name
        self.is_debug = is_debug
        self.is_precompute = is_precompute

        if is_precompute:
            self._mode = Mode.PRECOMPUTATION

        try:
            self._precompute_data = PrecomputeData(data_storage_name)
        except Exception as _:
            pass

        self._module_config = module_config
        self._develop_data = develop_data
        self._message_manager: MessageManager = MessageManager()
        self._communication_module: CommunicationModule = StandardCommunicationModule()

    def get_entity_id(self) -> EntityID:
        return self.agent_id

    def set_send_msg(self, connection_send_func: Callable) -> None:
        self.send_msg = connection_send_func

    def post_connect(self) -> None:
        if self.is_precompute:
            self._mode = Mode.PRECOMPUTATION
        else:
            if self._precompute_data.is_available():
                self._mode = Mode.PRECOMPUTED
            else:
                self._mode = Mode.NON_PRECOMPUTE

        self.config.set_value(ConfigKey.KEY_DEBUG_FLAG, self.is_debug)
        self.config.set_value(
            ConfigKey.KEY_DEVELOP_FLAG, self._develop_data.is_develop_mode()
        )
        self._ignore_time: int = int(
            self.config.get_value("kernel.agents.ignoreuntil", 3)
        )
        self._scenario_info: ScenarioInfo = ScenarioInfo(self.config, self._mode)
        self._world_info: WorldInfo = WorldInfo(self.world_model)
        self._agent_info = AgentInfo(self, self.world_model)
        self.logger = get_agent_logger(
            f"{self.__class__.__module__}.{self.__class__.__qualname__}",
            self._agent_info,
        )

        self.logger.debug(f"agent_config: {self.config}")

    def update_step_info(
        self, time: int, change_set: ChangeSet, hear: list[Command]
    ) -> None:
        self._agent_info.record_think_start_time()
        self._agent_info.set_time(time)

        if time == 1:
            self._message_manager.register_message_class(0, MessageAmbulanceTeam)
            self._message_manager.register_message_class(1, MessageFireBrigade)
            self._message_manager.register_message_class(2, MessagePoliceForce)
            self._message_manager.register_message_class(3, MessageBuilding)
            self._message_manager.register_message_class(4, MessageCivilian)
            self._message_manager.register_message_class(5, MessageRoad)
            self._message_manager.register_message_class(6, CommandAmbulance)
            self._message_manager.register_message_class(7, CommandFire)
            self._message_manager.register_message_class(8, CommandPolice)
            self._message_manager.register_message_class(9, CommandScout)
            self._message_manager.register_message_class(10, MessageReport)

        if time > self._ignore_time:
            self._message_manager.subscribe(
                self._agent_info, self._world_info, self._scenario_info
            )
            if not self._message_manager.get_is_subscribed():
                subscribed_channels = self._message_manager.get_subscribed_channels()
                if subscribed_channels:
                    self.logger.debug(
                        f"Subscribed channels: {subscribed_channels}",
                        message_manager=self._message_manager,
                    )
                    self.send_subscribe(time, subscribed_channels)
                    self._message_manager.set_is_subscribed(True)

        self._agent_info.set_heard_commands(hear)
        self._agent_info.set_change_set(change_set)
        self._world_info.set_change_set(change_set)

        self._message_manager.refresh()
        self._communication_module.receive(self, self._message_manager)

        self.think(time, change_set, hear)

        self.logger.debug(
            f"send messages: {self._message_manager.get_send_message_list()}",
            message_manager=self._message_manager,
        )

        self._message_manager.coordinate_message(
            self._agent_info, self._world_info, self._scenario_info
        )
        self._communication_module.send(self, self._message_manager)

    @abstractmethod
    def think(self, time: int, change_set: ChangeSet, hear: list[Command]) -> None:
        pass

    @abstractmethod
    def get_requested_entities(self) -> list[EntityURN]:
        pass

    def start_up(self, request_id: int) -> None:
        ak_connect = AKConnect()
        self.send_msg(ak_connect.write(request_id, self))

    def message_received(self, msg: Any) -> None:
        c_msg = ControlMessageFactory().make_message(msg)
        if isinstance(c_msg, KASense):
            self.handler_sense(c_msg)
        elif isinstance(c_msg, KAConnectOK):
            self.handle_connect_ok(c_msg)
        elif isinstance(c_msg, KAConnectError):
            self.handle_connect_error(c_msg)

    def handle_connect_error(self, msg: Any) -> NoReturn:
        if msg.reason.startswith("No more agents"):
            self.logger.debug(
                "Agent already connected: %s(request_id: %s)",
                msg.reason,
                msg.request_id,
            )
            self.finish_post_connect_event.set()
        else:
            self.logger.error(
                "Failed to connect agent: %s(request_id: %s)",
                msg.reason,
                msg.request_id,
            )
        sys.exit(1)

    def handle_connect_ok(self, msg: Any) -> None:
        self.agent_id = EntityID(msg.agent_id)
        self.world_model.add_entities(msg.world)
        config: RCRSConfig = msg.config
        self.config = Config()
        if config is not None:
            for key, value in config.data.items():
                self.config.set_value(key, value)
            for key, value in config.int_data.items():
                self.config.set_value(key, value)
            for key, value in config.float_data.items():
                self.config.set_value(key, value)
            for key, value in config.boolean_data.items():
                self.config.set_value(key, value)
            for key, value in config.array_data.items():
                self.config.set_value(key, value)
        self.send_acknowledge(msg.request_id)
        self.post_connect()
        self.logger.info(
            f"Connected to kernel: {self.__class__.__qualname__} (request_id: {msg.request_id}, agent_id: {self.agent_id}, mode: {self._mode})",
            request_id=msg.request_id,
        )
        if self.is_precompute:
            self.logger.info("Precompute finished")
            exit(0)

        self.finish_post_connect_event.set()

    def handler_sense(self, msg: Any) -> None:
        _id = EntityID(msg.agent_id)
        time = msg.time
        change_set = msg.change_set
        heard = msg.hear.commands

        if _id != self.get_entity_id():
            self.logger.error("Agent ID mismatch: %s != %s", _id, self.get_entity_id())
            return

        heard_commands: list[Command] = []
        for herad_command in heard:
            if herad_command.urn == CommandURN.AK_SPEAK:
                heard_commands.append(
                    AKSpeak(
                        herad_command.components[
                            ComponentControlMessageID.AgentID
                        ].entityID,
                        herad_command.components[
                            ComponentControlMessageID.Time
                        ].intValue,
                        herad_command.components[
                            ComponentCommandMessageID.Message
                        ].rawData,
                        herad_command.components[
                            ComponentCommandMessageID.Channel
                        ].intValue,
                    )
                )
        self.world_model.merge(change_set)
        start_update_info_time = _time.time()
        self.update_step_info(time, change_set, heard_commands)
        self.logger.debug(
            f"{time} step calculation time: {_time.time() - start_update_info_time}"
        )

    def send_acknowledge(self, request_id: int) -> None:
        ak_ack = AKAcknowledge()
        self.send_msg(ak_ack.write(request_id, self.agent_id))

    def send_clear(self, time: int, target: EntityID) -> None:
        cmd = AKClear(self.get_entity_id(), time, target)
        msg = cmd.prepare_cmd()
        self.send_msg(msg)

    def send_clear_area(self, time: int, x: int = -1, y: int = -1) -> None:
        cmd = AKClearArea(self.get_entity_id(), time, x, y)
        msg = cmd.prepare_cmd()
        self.send_msg(msg)

    def send_load(self, time: int, target: EntityID) -> None:
        cmd = AKLoad(self.get_entity_id(), time, target)
        msg = cmd.prepare_cmd()
        self.send_msg(msg)

    def send_move(self, time: int, path: list[int], x: int = -1, y: int = -1) -> None:
        cmd = AKMove(self.get_entity_id(), time, path[:], x, y)
        msg = cmd.prepare_cmd()
        self.send_msg(msg)

    def send_rescue(self, time: int, target: EntityID) -> None:
        cmd = AKRescue(self.get_entity_id(), time, target)
        msg = cmd.prepare_cmd()
        self.send_msg(msg)

    def send_rest(self, time: int) -> None:
        cmd = AKRest(self.get_entity_id(), time)
        msg = cmd.prepare_cmd()
        self.send_msg(msg)

    def send_say(self, time_step: int, message: str) -> None:
        cmd = AKSay(self.get_entity_id(), time_step, message)
        msg = cmd.prepare_cmd()
        self.send_msg(msg)

    def send_speak(self, time_step: int, message: bitarray, channel: int) -> None:
        cmd = AKSpeak(self.get_entity_id(), time_step, bytes(message), channel)  # type: ignore
        msg = cmd.prepare_cmd()
        self.send_msg(msg)

    def send_subscribe(self, time: int, channels: list[int]) -> None:
        cmd = AKSubscribe(self.get_entity_id(), time, channels)
        msg = cmd.prepare_cmd()
        self.send_msg(msg)

    def send_tell(self, time: int, message: str) -> None:
        cmd = AKTell(self.get_entity_id(), time, message)
        msg = cmd.prepare_cmd()
        self.send_msg(msg)

    def send_unload(self, time: int) -> None:
        cmd = AKUnload(self.get_entity_id(), time)
        msg = cmd.prepare_cmd()
        self.send_msg(msg)
