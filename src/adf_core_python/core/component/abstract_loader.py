from abc import ABC, abstractmethod
from typing import Optional

from adf_core_python.core.component.tactics.tactics_ambulance_center import (
    TacticsAmbulanceCenter,
)
from adf_core_python.core.component.tactics.tactics_ambulance_team import (
    TacticsAmbulanceTeam,
)
from adf_core_python.core.component.tactics.tactics_fire_brigade import (
    TacticsFireBrigade,
)
from adf_core_python.core.component.tactics.tactics_fire_station import (
    TacticsFireStation,
)
from adf_core_python.core.component.tactics.tactics_police_force import (
    TacticsPoliceForce,
)
from adf_core_python.core.component.tactics.tactics_police_office import (
    TacticsPoliceOffice,
)


class AbstractLoader(ABC):
    def __init__(self, team_name: Optional[str] = None):
        self._team_name: str = "" if team_name is None else team_name

    def get_team_name(self) -> str:
        return self._team_name

    @abstractmethod
    def get_tactics_ambulance_team(self) -> TacticsAmbulanceTeam:
        raise NotImplementedError

    @abstractmethod
    def get_tactics_fire_brigade(self) -> TacticsFireBrigade:
        raise NotImplementedError

    @abstractmethod
    def get_tactics_police_force(self) -> TacticsPoliceForce:
        raise NotImplementedError

    @abstractmethod
    def get_tactics_ambulance_center(self) -> TacticsAmbulanceCenter:
        raise NotImplementedError

    @abstractmethod
    def get_tactics_fire_station(self) -> TacticsFireStation:
        raise NotImplementedError

    @abstractmethod
    def get_tactics_police_office(self) -> TacticsPoliceOffice:
        raise NotImplementedError
