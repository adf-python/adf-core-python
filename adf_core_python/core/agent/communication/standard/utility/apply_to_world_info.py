from rcrs_core.entities.ambulanceTeam import AmbulanceTeam
from rcrs_core.entities.blockade import Blockade
from rcrs_core.entities.building import Building
from rcrs_core.entities.civilian import Civilian
from rcrs_core.entities.fireBrigade import FireBrigade
from rcrs_core.entities.policeForce import PoliceForce
from rcrs_core.entities.road import Road

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
from adf_core_python.core.agent.communication.standard.bundle.standard_message import (
    StandardMessage,
)
from adf_core_python.core.agent.info.world_info import WorldInfo


def apply_to_world_info(
    world_info: WorldInfo,
    standard_message: StandardMessage,
) -> None:
    """
    Apply to world info.

    PARAMETERS
    ----------
    world_info: WorldInfo
        The world info to apply to.
    standard_message: StandardMessage
        The standard message to apply to world info.
    """

    if isinstance(standard_message, MessageAmbulanceTeam):
        _apply_to_world_info_ambulance_team(world_info, standard_message)
    elif isinstance(standard_message, MessageFireBrigade):
        _apply_to_world_info_fire_brigade(world_info, standard_message)
    elif isinstance(standard_message, MessagePoliceForce):
        _apply_to_world_info_police_force(world_info, standard_message)
    elif isinstance(standard_message, MessageCivilian):
        _apply_to_world_info_civilian(world_info, standard_message)
    elif isinstance(standard_message, MessageBuilding):
        _apply_to_world_info_building(world_info, standard_message)
    elif isinstance(standard_message, MessageRoad):
        _apply_to_world_info_road(world_info, standard_message)
    else:
        return


def _apply_to_world_info_ambulance_team(
    world_info: WorldInfo,
    message_ambulance_team: MessageAmbulanceTeam,
) -> None:
    """
    Apply to world info for ambulance team.

    PARAMETERS
    ----------
    world_info: WorldInfo
        The world info to apply to.
    standard_message: StandardMessage
        The standard message to apply to world info.
    """
    entity_id = message_ambulance_team.get_ambulance_team_entity_id()
    if entity_id is None:
        return
    entity = world_info.get_entity(entity_id)
    if entity is None:
        ambulance = AmbulanceTeam(entity_id.get_value())
        if (hp := message_ambulance_team.get_ambulance_team_hp()) is not None:
            ambulance.set_hp(hp)
        if (damege := message_ambulance_team.get_ambulance_team_damage()) is not None:
            ambulance.set_damage(damege)
        if (
            buriedness := message_ambulance_team.get_ambulance_team_buriedness()
        ) is not None:
            ambulance.set_buriedness(buriedness)
        if (
            position := message_ambulance_team.get_ambulance_team_position()
        ) is not None:
            ambulance.set_position(position)
        world_info.add_entity(ambulance)
    else:
        if isinstance(entity, AmbulanceTeam):
            if (hp := message_ambulance_team.get_ambulance_team_hp()) is not None:
                entity.set_hp(hp)
            if (
                damege := message_ambulance_team.get_ambulance_team_damage()
            ) is not None:
                entity.set_damage(damege)
            if (
                buriedness := message_ambulance_team.get_ambulance_team_buriedness()
            ) is not None:
                entity.set_buriedness(buriedness)
            if (
                position := message_ambulance_team.get_ambulance_team_position()
            ) is not None:
                entity.set_position(position)


def _apply_to_world_info_fire_brigade(
    world_info: WorldInfo,
    message_fire_brigade: MessageFireBrigade,
) -> None:
    """
    Apply to world info for fire brigade.

    PARAMETERS
    ----------
    world_info: WorldInfo
        The world info to apply to.
    standard_message: StandardMessage
        The standard message to apply to world info.
    """
    entity_id = message_fire_brigade.get_fire_brigade_entity_id()
    if entity_id is None:
        return
    entity = world_info.get_entity(entity_id)
    if entity is None:
        fire_brigade = FireBrigade(entity_id.get_value())
        if (hp := message_fire_brigade.get_fire_brigade_hp()) is not None:
            fire_brigade.set_hp(hp)
        if (damage := message_fire_brigade.get_fire_brigade_damage()) is not None:
            fire_brigade.set_damage(damage)
        if (
            buriedness := message_fire_brigade.get_fire_brigade_buriedness()
        ) is not None:
            fire_brigade.set_buriedness(buriedness)
        if (position := message_fire_brigade.get_fire_brigade_position()) is not None:
            fire_brigade.set_position(position)
        if (water := message_fire_brigade.get_fire_brigade_water()) is not None:
            fire_brigade.set_water(water)
        world_info.add_entity(fire_brigade)
    else:
        if isinstance(entity, FireBrigade):
            if (hp := message_fire_brigade.get_fire_brigade_hp()) is not None:
                entity.set_hp(hp)
            if (damage := message_fire_brigade.get_fire_brigade_damage()) is not None:
                entity.set_damage(damage)
            if (
                buriedness := message_fire_brigade.get_fire_brigade_buriedness()
            ) is not None:
                entity.set_buriedness(buriedness)
            if (
                position := message_fire_brigade.get_fire_brigade_position()
            ) is not None:
                entity.set_position(position)
            if (water := message_fire_brigade.get_fire_brigade_water()) is not None:
                entity.set_water(water)


def _apply_to_world_info_police_force(
    world_info: WorldInfo,
    message_police_force: MessagePoliceForce,
) -> None:
    """
    Apply to world info for police force.

    PARAMETERS
    ----------
    world_info: WorldInfo
        The world info to apply to.
    standard_message: StandardMessage
        The standard message to apply to world info.
    """
    entity_id = message_police_force.get_police_force_entity_id()
    if entity_id is None:
        return
    entity = world_info.get_entity(entity_id)
    if entity is None:
        police_force = PoliceForce(entity_id.get_value())
        if (hp := message_police_force.get_police_force_hp()) is not None:
            police_force.set_hp(hp)
        if (damage := message_police_force.get_police_force_damage()) is not None:
            police_force.set_damage(damage)
        if (
            buriedness := message_police_force.get_police_force_buriedness()
        ) is not None:
            police_force.set_buriedness(buriedness)
        if (position := message_police_force.get_police_force_position()) is not None:
            police_force.set_position(position)
        world_info.add_entity(police_force)
    else:
        if isinstance(entity, PoliceForce):
            if (hp := message_police_force.get_police_force_hp()) is not None:
                entity.set_hp(hp)
            if (damage := message_police_force.get_police_force_damage()) is not None:
                entity.set_damage(damage)
            if (
                buriedness := message_police_force.get_police_force_buriedness()
            ) is not None:
                entity.set_buriedness(buriedness)
            if (
                position := message_police_force.get_police_force_position()
            ) is not None:
                entity.set_position(position)


def _apply_to_world_info_civilian(
    world_info: WorldInfo,
    message_civilian: MessageCivilian,
) -> None:
    """
    Apply to world info for civilian.

    PARAMETERS
    ----------
    world_info: WorldInfo
        The world info to apply to.
    standard_message: StandardMessage
        The standard message to apply to world info.
    """
    entity_id = message_civilian.get_civilian_entity_id()
    if entity_id is None:
        return
    entity = world_info.get_entity(entity_id)
    if entity is None:
        civilian = Civilian(entity_id.get_value())
        if (hp := message_civilian.get_civilian_hp()) is not None:
            civilian.set_hp(hp)
        if (damage := message_civilian.get_civilian_damage()) is not None:
            civilian.set_damage(damage)
        if (buriedness := message_civilian.get_civilian_buriedness()) is not None:
            civilian.set_buriedness(buriedness)
        if (position := message_civilian.get_civilian_position()) is not None:
            civilian.set_position(position)
        world_info.add_entity(civilian)
    else:
        if isinstance(entity, Civilian):
            if (hp := message_civilian.get_civilian_hp()) is not None:
                entity.set_hp(hp)
            if (damage := message_civilian.get_civilian_damage()) is not None:
                entity.set_damage(damage)
            if (buriedness := message_civilian.get_civilian_buriedness()) is not None:
                entity.set_buriedness(buriedness)
            if (position := message_civilian.get_civilian_position()) is not None:
                entity.set_position(position)


def _apply_to_world_info_building(
    world_info: WorldInfo,
    message_building: MessageBuilding,
) -> None:
    """
    Apply to world info for building.

    PARAMETERS
    ----------
    world_info: WorldInfo
        The world info to apply to.
    standard_message: StandardMessage
        The standard message to apply to world info.
    """
    entity_id = message_building.get_building_entity_id()
    if entity_id is None:
        return
    entity = world_info.get_entity(entity_id)
    if entity is None:
        building = Building(entity_id.get_value())
        if (fieryness := message_building.get_building_fireyness()) is not None:
            building.set_fieryness(fieryness)
        if (brokenness := message_building.get_building_brokenness()) is not None:
            building.set_brokenness(brokenness)
        if (temperature := message_building.get_building_temperature()) is not None:
            building.set_temperature(temperature)
        world_info.add_entity(building)
    else:
        if isinstance(entity, Building):
            if (fieryness := message_building.get_building_fireyness()) is not None:
                entity.set_fieryness(fieryness)
            if (brokenness := message_building.get_building_brokenness()) is not None:
                entity.set_brokenness(brokenness)
            if (temperature := message_building.get_building_temperature()) is not None:
                entity.set_temperature(temperature)


def _apply_to_world_info_road(
    world_info: WorldInfo,
    message_road: MessageRoad,
) -> None:
    """
    Apply to world info for road.

    PARAMETERS
    ----------
    world_info: WorldInfo
        The world info to apply to.
    standard_message: StandardMessage
        The standard message to apply to world info.
    """
    entity_id = message_road.get_road_entity_id()
    if entity_id is None:
        return
    entity = world_info.get_entity(entity_id)
    if not isinstance(entity, Road):
        return

    blockade_entity_id = message_road.get_road_blockade_entity_id()
    if blockade_entity_id is None:
        return

    blockade = world_info.get_entity(blockade_entity_id)
    if blockade is None:
        road_blockade = Blockade(blockade_entity_id.get_value())
        if (repair_cost := message_road.get_road_blockade_repair_cost()) is not None:
            road_blockade.set_repaire_cost(repair_cost)
        if (x := message_road.get_road_blockade_x()) is not None:
            road_blockade.set_x(x)
        if (y := message_road.get_road_blockade_y()) is not None:
            road_blockade.set_y(y)
        world_info.add_entity(road_blockade)
    else:
        if isinstance(blockade, Blockade):
            if (
                repair_cost := message_road.get_road_blockade_repair_cost()
            ) is not None:
                blockade.set_repaire_cost(repair_cost)
            if (x := message_road.get_road_blockade_x()) is not None:
                blockade.set_x(x)
            if (y := message_road.get_road_blockade_y()) is not None:
                blockade.set_y(y)
