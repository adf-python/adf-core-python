from adf_core_python.core.component import AbstractLoader
from adf_core_python.core.component.tactics import (
  TacticsAmbulanceCenter,
  TacticsAmbulanceTeam,
  TacticsFireBrigade,
  TacticsFireStation,
  TacticsPoliceForce,
  TacticsPoliceOffice,
)
from adf_core_python.implement.tactics import (
  DefaultTacticsAmbulanceCenter,
  DefaultTacticsAmbulanceTeam,
  DefaultTacticsFireBrigade,
  DefaultTacticsFireStation,
  DefaultTacticsPoliceForce,
  DefaultTacticsPoliceOffice,
)


class DefaultLoader(AbstractLoader):
  def get_tactics_ambulance_team(self) -> TacticsAmbulanceTeam:
    return DefaultTacticsAmbulanceTeam()

  def get_tactics_fire_brigade(self) -> TacticsFireBrigade:
    return DefaultTacticsFireBrigade()

  def get_tactics_police_force(self) -> TacticsPoliceForce:
    return DefaultTacticsPoliceForce()

  def get_tactics_ambulance_center(self) -> TacticsAmbulanceCenter:
    return DefaultTacticsAmbulanceCenter()

  def get_tactics_fire_station(self) -> TacticsFireStation:
    return DefaultTacticsFireStation()

  def get_tactics_police_office(self) -> TacticsPoliceOffice:
    return DefaultTacticsPoliceOffice()
